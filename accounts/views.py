from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.utils.crypto import get_random_string
from .models import UserProfile
from products.models import Package
from orders.models import Order
from wallet.models import WithdrawalRequest, Transaction
from support.models import SupportRequest


DEFAULT_REFERRAL_CODE = '1'  # اگر معرف نداشته باشد، به این کد وصل می‌شود


class LeadRegisterForm(forms.Form):
    """فرم محدود ثبت بسته از طریق لینک معرف — فقط نام، شماره و صنف کاری"""
    first_name = forms.CharField(
        max_length=30, required=True, label='نام',
        widget=forms.TextInput(attrs={
            'class': 'field', 'placeholder': 'مثلاً علی', 'autocomplete': 'given-name'
        })
    )
    last_name = forms.CharField(
        max_length=30, required=True, label='نام خانوادگی',
        widget=forms.TextInput(attrs={
            'class': 'field', 'placeholder': 'مثلاً رضایی', 'autocomplete': 'family-name'
        })
    )
    phone = forms.CharField(
        max_length=11, required=True, label='شماره موبایل',
        widget=forms.TextInput(attrs={
            'class': 'field', 'placeholder': '0912xxxxxxx',
            'inputmode': 'numeric', 'maxlength': '11', 'autocomplete': 'tel'
        })
    )
    job_class = forms.CharField(
        max_length=100, required=True, label='صنف کاری',
        widget=forms.TextInput(attrs={
            'class': 'field', 'placeholder': 'مثلاً پوشاک، لوازم خانگی، خدمات زیبایی و ...'
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip().replace(' ', '').replace('-', '')
        if not phone.isdigit() or len(phone) != 11 or not phone.startswith('09'):
            raise forms.ValidationError('شماره موبایل معتبر وارد کنید (۱۱ رقم و با ۰۹ شروع شود).')
        if User.objects.filter(username=phone).exists() or UserProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('این شماره قبلاً ثبت شده است. با پشتیبانی تماس بگیرید.')
        return phone


def home(request):
    packages = Package.objects.filter(is_active=True)[:6]
    return render(request, 'home.html', {'packages': packages})


def _resolve_referrer(ref_code: str):
    """
    پیدا کردن پروفایل معرف.
    اگر کد خالی باشد یا پیدا نشود، به کد پیش‌فرض DEFAULT_REFERRAL_CODE وصل می‌شود.
    """
    code = (ref_code or '').strip().upper()
    if not code:
        code = DEFAULT_REFERRAL_CODE
    try:
        return UserProfile.objects.get(referral_code=code)
    except UserProfile.DoesNotExist:
        # تلاش با کد پیش‌فرض
        if code != DEFAULT_REFERRAL_CODE:
            try:
                return UserProfile.objects.get(referral_code=DEFAULT_REFERRAL_CODE)
            except UserProfile.DoesNotExist:
                return None
        return None


def register_view(request):
    """
    ثبت بسته از طریق لینک معرف.
    کاربر فقط نام، شماره و صنف کاری را وارد می‌کند.
    اگر معرف نداشته باشد، به کد «1» وصل می‌شود.
    """
    ref_code = request.GET.get('ref') or request.session.get('ref_code', '')
    if request.method == 'POST':
        form = LeadRegisterForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            job_class = form.cleaned_data['job_class']

            user = User.objects.create_user(
                username=phone,
                password=get_random_string(32),
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )
            user.set_unusable_password()
            user.save()

            profile = user.profile
            profile.phone = phone
            profile.job_class = job_class
            profile.status = 'pending'

            # تعیین معرف: کد از لینک، در غیر این صورت کد پیش‌فرض «1»
            referrer = _resolve_referrer(ref_code)
            if referrer and referrer.user_id != user.id:
                profile.referred_by = referrer
            profile.save()

            if 'ref_code' in request.session:
                del request.session['ref_code']

            messages.success(
                request,
                'بسته شما با موفقیت ثبت شد. تیم ما به زودی وضعیت را بررسی می‌کند.'
            )
            return redirect('register_success')
    else:
        form = LeadRegisterForm()
        if ref_code:
            request.session['ref_code'] = ref_code.upper()

    display_ref = (ref_code or '').strip().upper() or DEFAULT_REFERRAL_CODE
    return render(request, 'registration/register.html', {
        'form': form,
        'ref_code': display_ref if ref_code else '',
    })


def register_success(request):
    return render(request, 'registration/register_success.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'خوش آمدید {user.first_name or user.username}!')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    form.fields['username'].label = 'نام کاربری / شماره موبایل'
    form.fields['password'].label = 'رمز عبور'
    return render(request, 'registration/login.html', {'form': form})


@login_required
def dashboard(request):
    profile = request.user.profile
    recent_orders = Order.objects.filter(referrer=request.user, status='paid').select_related('buyer', 'package')[:10]
    my_orders = Order.objects.filter(buyer=request.user).select_related('package')[:5]
    total_commission = sum(
        o.commission_amount for o in Order.objects.filter(referrer=request.user, status='paid')
    )
    referred_count = UserProfile.objects.filter(referred_by=profile).count()
    context = {
        'profile': profile,
        'recent_orders': recent_orders,
        'my_orders': my_orders,
        'total_commission': total_commission,
        'referred_count': referred_count,
        'packages': Package.objects.filter(is_active=True),
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def referral_page(request):
    profile = request.user.profile
    referred_users = UserProfile.objects.filter(referred_by=profile).select_related('user')
    sales = Order.objects.filter(referrer=request.user, status='paid').select_related('buyer', 'package')
    return render(request, 'dashboard/referral.html', {
        'profile': profile,
        'referred_users': referred_users,
        'sales': sales,
    })


@login_required
def wallet_page(request):
    profile = request.user.profile
    transactions = Transaction.objects.filter(user=request.user)[:20]
    withdrawals = WithdrawalRequest.objects.filter(user=request.user)[:10]
    return render(request, 'dashboard/wallet.html', {
        'profile': profile,
        'transactions': transactions,
        'withdrawals': withdrawals,
    })


@login_required
def request_withdrawal(request):
    profile = request.user.profile
    if not profile.can_withdraw:
        messages.error(request, 'فقط کاربران سطح طلایی می‌توانند درخواست برداشت دهند.')
        return redirect('wallet')
    if request.method == 'POST':
        amount = int(request.POST.get('amount', 0))
        bank_card = request.POST.get('bank_card', '').replace(' ', '').replace('-', '')
        if amount < 50000:
            messages.error(request, 'حداقل مبلغ برداشت ۵۰,۰۰۰ تومان است.')
        elif amount > profile.wallet_balance:
            messages.error(request, 'موجودی کافی نیست.')
        elif len(bank_card) != 16 or not bank_card.isdigit():
            messages.error(request, 'شماره کارت نامعتبر است.')
        else:
            WithdrawalRequest.objects.create(
                user=request.user, amount=amount, bank_card=bank_card
            )
            messages.success(request, 'درخواست برداشت با موفقیت ثبت شد.')
            return redirect('wallet')
    return render(request, 'dashboard/withdraw.html', {'profile': profile})


@login_required
def support_request(request):
    profile = request.user.profile
    packages = Package.objects.filter(is_active=True)
    if request.method == 'POST':
        package_id = request.POST.get('package')
        package = get_object_or_404(Package, id=package_id)
        if profile.points < package.support_price:
            messages.error(request, f'امتیاز شما ({profile.points:,}) کمتر از قیمت پشتیبانی ({package.support_price:,}) است.')
        else:
            SupportRequest.objects.create(
                user=request.user, package=package, points_used=package.support_price
            )
            profile.points -= package.support_price
            profile.save(update_fields=['points'])
            messages.success(request, 'درخواست تمدید پشتیبانی ثبت شد.')
            return redirect('dashboard')
    return render(request, 'dashboard/support.html', {'profile': profile, 'packages': packages})


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        profile.phone = request.POST.get('phone', '')
        profile.bank_card = request.POST.get('bank_card', '').replace(' ', '')
        profile.job_class = request.POST.get('job_class', profile.job_class)
        profile.save()
        messages.success(request, 'پروفایل به‌روزرسانی شد.')
        return redirect('dashboard')
    return render(request, 'dashboard/profile.html', {'profile': profile})

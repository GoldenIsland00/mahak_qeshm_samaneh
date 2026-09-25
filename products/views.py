from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Package
from orders.models import Order


def package_list(request):
    packages = Package.objects.filter(is_active=True)
    return render(request, 'products/list.html', {'packages': packages})


def package_detail(request, slug):
    package = get_object_or_404(Package, slug=slug, is_active=True)
    return render(request, 'products/detail.html', {'package': package})


@login_required
def buy_package(request, slug):
    package = get_object_or_404(Package, slug=slug, is_active=True)
    profile = request.user.profile

    # خرید با امتیاز (نقره‌ای و طلایی)
    if request.method == 'POST' and request.POST.get('pay_with_points') == '1':
        if profile.level == 'bronze':
            messages.error(request, 'در سطح برنزی فقط می‌توانید با پول خرید کنید یا درخواست پشتیبانی دهید.')
            return redirect('package_detail', slug=slug)
        if profile.points < package.price:
            messages.error(request, 'امتیاز کافی ندارید.')
            return redirect('package_detail', slug=slug)
        profile.points -= package.price
        profile.save(update_fields=['points'])
        # معرف خودکار از پروفایل
        referrer = profile.referred_by.user if profile.referred_by else None
        order = Order.objects.create(
            buyer=request.user, package=package, amount=package.price,
            referrer=referrer, status='paid', paid_at=timezone.now()
        )
        # کمیسیون برای معرف
        if referrer and hasattr(referrer, 'profile'):
            commission = referrer.profile.add_commission(package.price)
            order.commission_amount = commission
            order.save(update_fields=['commission_amount'])
        messages.success(request, f'بسته {package.name} با موفقیت با امتیاز خریداری شد!')
        return redirect('dashboard')

    # خرید عادی
    if request.method == 'POST':
        referrer = profile.referred_by.user if profile.referred_by else None
        order = Order.objects.create(
            buyer=request.user, package=package, amount=package.price, referrer=referrer
        )
        # دمو: مستقیم پرداخت
        order.mark_as_paid()
        messages.success(request, f'خرید موفق! کد پیگیری: {order.tracking_code}')
        return redirect('dashboard')

    return render(request, 'products/buy.html', {'package': package, 'profile': profile})

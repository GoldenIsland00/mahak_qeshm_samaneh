from django.shortcuts import redirect
from accounts.models import UserProfile
from .models import ReferralClick


def track_referral(request, code):
    """وقتی کسی روی لینک معرف کلیک می‌کند"""
    code = code.upper().strip()
    try:
        profile = UserProfile.objects.get(referral_code=code)
        # ذخیره در session برای ۳۰ روز
        request.session['ref_code'] = code
        request.session.set_expiry(60 * 60 * 24 * 30)
        # ثبت کلیک
        ReferralClick.objects.create(
            referral_code=code,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=(request.META.get('HTTP_USER_AGENT') or '')[:500]
        )
    except UserProfile.DoesNotExist:
        pass
    return redirect('register')

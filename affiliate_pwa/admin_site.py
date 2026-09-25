from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from orders.models import Order
from wallet.models import WithdrawalRequest
from django.db.models import Sum


class AffiliateAdminSite(AdminSite):
    site_header = 'پنل مدیریت افیلیت پرو'
    site_title = 'افیلیت پرو'
    index_title = 'داشبورد مدیریت'

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['unread_withdrawals'] = WithdrawalRequest.objects.filter(status='unread').count()
        extra_context['total_users'] = User.objects.count()
        extra_context['total_orders'] = Order.objects.filter(status='paid').count()
        extra_context['total_commission'] = (
            Order.objects.filter(status='paid').aggregate(s=Sum('commission_amount'))['s'] or 0
        )
        return super().index(request, extra_context=extra_context)


# Use default for simplicity - override index via template + context processor alternative
# We'll patch via AppConfig ready instead

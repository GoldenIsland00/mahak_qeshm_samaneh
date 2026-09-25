from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'حساب‌ها و کاربران'

    def ready(self):
        # Patch admin index to show stats
        from django.contrib import admin
        original_index = admin.site.index

        def index_with_stats(request, extra_context=None):
            from wallet.models import WithdrawalRequest
            from django.contrib.auth.models import User
            from orders.models import Order
            from django.db.models import Sum
            extra_context = extra_context or {}
            try:
                extra_context['unread_withdrawals'] = WithdrawalRequest.objects.filter(status='unread').count()
                extra_context['total_users'] = User.objects.count()
                extra_context['total_orders'] = Order.objects.filter(status='paid').count()
                extra_context['total_commission'] = (
                    Order.objects.filter(status='paid').aggregate(s=Sum('commission_amount'))['s'] or 0
                )
            except Exception:
                pass
            return original_index(request, extra_context=extra_context)

        admin.site.index = index_with_stats
        admin.site.site_header = '🚀 پنل مدیریت افیلیت پرو'
        admin.site.site_title = 'افیلیت پرو'
        admin.site.index_title = 'داشبورد مدیریت'

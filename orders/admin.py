from django.contrib import admin
from django.utils.html import format_html
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'buyer_link', 'package', 'amount_display', 'referrer_link', 'commission_display', 'status_badge', 'created_at')
    list_filter = ('status', 'created_at', 'package')
    search_fields = ('tracking_code', 'buyer__username', 'buyer__email', 'buyer__first_name', 'referrer__username')
    readonly_fields = ('tracking_code', 'commission_amount', 'created_at', 'paid_at')
    raw_id_fields = ('buyer', 'referrer')
    actions = ['mark_paid']
    list_per_page = 25
    date_hierarchy = 'created_at'

    def buyer_link(self, obj):
        return format_html('<a href="/admin/auth/user/{}/change/">{}</a>', obj.buyer.id, obj.buyer.get_full_name() or obj.buyer.username)
    buyer_link.short_description = 'خریدار'

    def referrer_link(self, obj):
        if obj.referrer:
            return format_html(
                '<a href="/admin/auth/user/{}/change/" style="color:#4f46e5; font-weight:bold;">{}</a>',
                obj.referrer.id, obj.referrer.get_full_name() or obj.referrer.username
            )
        return format_html('<span style="color:#999;">—</span>')
    referrer_link.short_description = 'عامل / معرف'

    def amount_display(self, obj):
        return f"{obj.amount:,}"
    amount_display.short_description = 'مبلغ'
    amount_display.admin_order_field = 'amount'

    def commission_display(self, obj):
        if obj.commission_amount:
            return format_html('<span style="color:#16a34a; font-weight:bold;">+{:,}</span>', obj.commission_amount)
        return '—'
    commission_display.short_description = 'کمیسیون'

    def status_badge(self, obj):
        colors = {'pending': '#f59e0b', 'paid': '#16a34a', 'cancelled': '#ef4444', 'refunded': '#6b7280'}
        labels = dict(Order.STATUS_CHOICES)
        return format_html(
            '<span style="background:{}; color:white; padding:2px 8px; border-radius:8px; font-size:11px;">{}</span>',
            colors.get(obj.status, '#999'), labels.get(obj.status, obj.status)
        )
    status_badge.short_description = 'وضعیت'

    @admin.action(description='علامت‌گذاری به عنوان پرداخت‌شده + محاسبه کمیسیون')
    def mark_paid(self, request, queryset):
        count = 0
        for order in queryset.filter(status='pending'):
            order.mark_as_paid()
            count += 1
        self.message_user(request, f'{count} سفارش پرداخت شد و کمیسیون محاسبه گردید.')

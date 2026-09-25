from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Sum
from .models import Transaction, WithdrawalRequest


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type_badge', 'amount_display', 'balance_after', 'description', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 30

    def type_badge(self, obj):
        colors = {
            'commission': '#16a34a', 'purchase': '#2563eb',
            'withdrawal': '#dc2626', 'support': '#ca8a04', 'bonus': '#7c3aed'
        }
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:6px;font-size:11px;">{}</span>',
            colors.get(obj.type, '#666'), obj.get_type_display()
        )
    type_badge.short_description = 'نوع'

    def amount_display(self, obj):
        color = '#16a34a' if obj.amount > 0 else '#dc2626'
        sign = '+' if obj.amount > 0 else ''
        return format_html('<span style="color:{};font-weight:bold;">{}{:,}</span>', color, sign, obj.amount)
    amount_display.short_description = 'مبلغ'


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_link', 'amount_display', 'bank_card_display', 'status_badge', 'created_at', 'processed_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'bank_card')
    readonly_fields = ('created_at', 'processed_at', 'user', 'amount', 'bank_card')
    list_per_page = 25
    date_hierarchy = 'created_at'
    actions = ['mark_read', 'approve_requests', 'reject_requests', 'mark_paid']
    fieldsets = (
        ('اطلاعات درخواست', {
            'fields': ('user', 'amount', 'bank_card', 'created_at')
        }),
        ('وضعیت و پردازش', {
            'fields': ('status', 'admin_note', 'processed_at')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'user__profile')

    def user_link(self, obj):
        name = obj.user.get_full_name() or obj.user.username
        wallet = obj.user.profile.wallet_balance if hasattr(obj.user, 'profile') else 0
        return format_html(
            '<a href="/admin/auth/user/{}/change/"><strong>{}</strong></a><br>'
            '<small style="color:#666;">موجودی: {:,} تومان</small>',
            obj.user.id, name, wallet
        )
    user_link.short_description = 'کاربر'

    def amount_display(self, obj):
        return format_html('<strong style="font-size:14px;">{:,}</strong> تومان', obj.amount)
    amount_display.short_description = 'مبلغ'
    amount_display.admin_order_field = 'amount'

    def bank_card_display(self, obj):
        c = obj.bank_card
        if len(c) == 16:
            return f"{c[:4]}-{c[4:8]}-{c[8:12]}-{c[12:]}"
        return c
    bank_card_display.short_description = 'شماره کارت'

    def status_badge(self, obj):
        styles = {
            'unread': ('#dc2626', '#fff', 'خوانده‌نشده'),
            'read': ('#f59e0b', '#111', 'خوانده‌شده'),
            'approved': ('#16a34a', '#fff', 'تأیید شده'),
            'rejected': ('#6b7280', '#fff', 'رد شده'),
            'paid': ('#2563eb', '#fff', 'پرداخت شده'),
        }
        bg, color, label = styles.get(obj.status, ('#999', '#fff', obj.status))
        return format_html(
            '<span style="background:{};color:{};padding:4px 12px;border-radius:10px;font-size:12px;font-weight:bold;">{}</span>',
            bg, color, label
        )
    status_badge.short_description = 'وضعیت'
    status_badge.admin_order_field = 'status'

    def changelist_view(self, request, extra_context=None):
        # Auto mark as read when admin opens the list? No - only via action
        extra_context = extra_context or {}
        unread = WithdrawalRequest.objects.filter(status='unread').count()
        extra_context['unread_count'] = unread
        return super().changelist_view(request, extra_context)

    @admin.action(description='👁 علامت‌گذاری به عنوان خوانده‌شده')
    def mark_read(self, request, queryset):
        updated = queryset.filter(status='unread').update(status='read', is_seen=True)
        self.message_user(request, f'{updated} درخواست به خوانده‌شده تغییر کرد.')

    @admin.action(description='✅ تأیید درخواست (کسر از کیف پول)')
    def approve_requests(self, request, queryset):
        count = 0
        for w in queryset.filter(status__in=['unread', 'read']):
            profile = w.user.profile
            if profile.wallet_balance >= w.amount:
                profile.wallet_balance -= w.amount
                profile.save(update_fields=['wallet_balance'])
                Transaction.objects.create(
                    user=w.user,
                    amount=-w.amount,
                    type='withdrawal',
                    description=f'برداشت به کارت {w.bank_card}',
                    balance_after=profile.wallet_balance
                )
                w.status = 'approved'
                w.processed_at = timezone.now()
                w.is_seen = True
                w.save()
                count += 1
            else:
                messages.warning(request, f'موجودی {w.user.username} کافی نیست.')
        self.message_user(request, f'{count} درخواست تأیید و از کیف پول کسر شد.')

    @admin.action(description='❌ رد درخواست')
    def reject_requests(self, request, queryset):
        updated = queryset.filter(status__in=['unread', 'read']).update(
            status='rejected', processed_at=timezone.now(), is_seen=True
        )
        self.message_user(request, f'{updated} درخواست رد شد.')

    @admin.action(description='💰 علامت‌گذاری به عنوان پرداخت‌شده')
    def mark_paid(self, request, queryset):
        updated = queryset.filter(status='approved').update(
            status='paid', processed_at=timezone.now()
        )
        self.message_user(request, f'{updated} درخواست پرداخت‌شده شد.')

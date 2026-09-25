from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import SupportRequest


@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'points_used', 'status_badge', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__first_name')
    actions = ['approve', 'reject']
    readonly_fields = ('user', 'package', 'points_used', 'created_at')

    def status_badge(self, obj):
        styles = {
            'pending': ('#f59e0b', 'در انتظار'),
            'approved': ('#16a34a', 'تأیید شده'),
            'rejected': ('#dc2626', 'رد شده'),
        }
        bg, label = styles.get(obj.status, ('#999', obj.status))
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:8px;font-size:11px;">{}</span>',
            bg, label
        )
    status_badge.short_description = 'وضعیت'

    @admin.action(description='تأیید')
    def approve(self, request, queryset):
        queryset.filter(status='pending').update(status='approved', processed_at=timezone.now())
        self.message_user(request, 'درخواست‌ها تأیید شدند.')

    @admin.action(description='رد')
    def reject(self, request, queryset):
        queryset.filter(status='pending').update(status='rejected', processed_at=timezone.now())
        self.message_user(request, 'درخواست‌ها رد شدند.')

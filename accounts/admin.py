from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db.models import Count
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'پروفایل و وضعیت'
    fk_name = 'user'
    fields = (
        ('referral_code', 'referred_by'),
        ('level', 'status', 'purchase_date'),
        ('job_class', 'phone'),
        ('points', 'total_sales', 'wallet_balance'),
        ('national_id', 'bank_card'),
        'admin_note',
    )
    readonly_fields = ('referral_code',)
    extra = 0


class StatusFilter(admin.SimpleListFilter):
    title = 'وضعیت بررسی'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('pending', '🔴 بررسی‌نشده'),
            ('reviewed', '🟡 بررسی‌شده'),
            ('purchased', '🟢 خریده'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(profile__status=self.value())
        return queryset


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = (
        'username',
        'get_full_name_display',
        'get_phone',
        'get_job_class',
        'get_status_badge',
        'get_level_badge',
        'get_purchase_date',
        'get_referrer',
        'is_staff_display',
        'date_joined',
    )
    list_filter = (
        StatusFilter,
        'is_staff',
        'is_superuser',
        'is_active',
        'profile__level',
        'date_joined',
    )
    search_fields = (
        'username', 'email', 'first_name', 'last_name',
        'profile__referral_code', 'profile__phone', 'profile__job_class',
    )
    ordering = ('-date_joined',)
    list_per_page = 40
    actions = [
        'make_staff',
        'remove_staff',
        'set_status_pending',
        'set_status_reviewed',
        'set_status_purchased',
        'activate_users',
        'deactivate_users',
    ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email')}),
        ('دسترسی‌ها', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': 'برای تبدیل کاربر به ادمین، تیک «وضعیت کارکنان» را بزنید.',
        }),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'is_staff', 'is_active'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('profile', 'profile__referred_by', 'profile__referred_by__user')

    def get_full_name_display(self, obj):
        name = obj.get_full_name()
        return name if name else format_html('<span style="color:#999;">—</span>')
    get_full_name_display.short_description = 'نام کامل'
    get_full_name_display.admin_order_field = 'first_name'

    def get_phone(self, obj):
        if hasattr(obj, 'profile') and obj.profile.phone:
            return obj.profile.phone
        return format_html('<span style="color:#999;">—</span>')
    get_phone.short_description = 'موبایل'
    get_phone.admin_order_field = 'profile__phone'

    def get_job_class(self, obj):
        if hasattr(obj, 'profile') and obj.profile.job_class:
            return obj.profile.job_class
        return format_html('<span style="color:#999;">—</span>')
    get_job_class.short_description = 'صنف کاری'
    get_job_class.admin_order_field = 'profile__job_class'

    def get_status_badge(self, obj):
        if not hasattr(obj, 'profile'):
            return '-'
        status = obj.profile.status
        colors = {
            'pending': ('#fef2f2', '#dc2626', '🔴 بررسی‌نشده'),
            'reviewed': ('#fefce8', '#ca8a04', '🟡 بررسی‌شده'),
            'purchased': ('#f0fdf4', '#16a34a', '🟢 خریده'),
        }
        bg, color, label = colors.get(status, ('#f3f4f6', '#6b7280', status))
        return format_html(
            '<span style="background:{}; color:{}; padding:4px 12px; border-radius:20px; '
            'font-size:12px; font-weight:700; display:inline-block; min-width:100px; text-align:center;">{}</span>',
            bg, color, label
        )
    get_status_badge.short_description = 'وضعیت'
    get_status_badge.admin_order_field = 'profile__status'

    def get_level_badge(self, obj):
        if not hasattr(obj, 'profile'):
            return '-'
        colors = {'bronze': '#cd7f32', 'silver': '#a0a0a0', 'gold': '#ffd700'}
        labels = {'bronze': '🥉 برنزی', 'silver': '🥈 نقره‌ای', 'gold': '🥇 طلایی'}
        level = obj.profile.level
        return format_html(
            '<span style="background:{}; color:#111; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:bold;">{}</span>',
            colors.get(level, '#999'), labels.get(level, level)
        )
    get_level_badge.short_description = 'سطح'
    get_level_badge.admin_order_field = 'profile__level'

    def get_purchase_date(self, obj):
        if hasattr(obj, 'profile') and obj.profile.purchase_date:
            return obj.profile.purchase_date.strftime('%Y/%m/%d')
        return format_html('<span style="color:#999;">—</span>')
    get_purchase_date.short_description = 'تاریخ خرید'
    get_purchase_date.admin_order_field = 'profile__purchase_date'

    def get_referrer(self, obj):
        if hasattr(obj, 'profile') and obj.profile.referred_by:
            ref = obj.profile.referred_by
            return format_html(
                '<a href="/admin/auth/user/{}/change/">{}</a> <small style="color:#666;">({})</small>',
                ref.user.id, ref.user.get_full_name() or ref.user.username, ref.referral_code
            )
        return format_html('<span style="color:#999;">—</span>')
    get_referrer.short_description = 'معرف'

    def is_staff_display(self, obj):
        if obj.is_superuser:
            return format_html(
                '<span style="background:#4f46e5; color:white; padding:3px 10px; border-radius:10px; font-size:11px; font-weight:bold;">👑 سوپرادمین</span>'
            )
        if obj.is_staff:
            return format_html(
                '<span style="background:#6366f1; color:white; padding:3px 10px; border-radius:10px; font-size:11px; font-weight:bold;">✓ ادمین</span>'
            )
        return format_html('<span style="color:#999; font-size:12px;">کاربر</span>')
    is_staff_display.short_description = 'نقش'
    is_staff_display.admin_order_field = 'is_staff'

    # ——— Actions ———
    @admin.action(description='✅ تبدیل به ادمین (is_staff)')
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f'{updated} کاربر به ادمین تبدیل شدند.')

    @admin.action(description='❌ حذف دسترسی ادمین')
    def remove_staff(self, request, queryset):
        updated = queryset.exclude(is_superuser=True).update(is_staff=False)
        self.message_user(request, f'{updated} کاربر از ادمین خارج شدند.')

    @admin.action(description='🔴 تنظیم وضعیت: بررسی‌نشده')
    def set_status_pending(self, request, queryset):
        count = 0
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.status = 'pending'
                user.profile.save(update_fields=['status'])
                count += 1
        self.message_user(request, f'وضعیت {count} کاربر به «بررسی‌نشده» تغییر کرد.')

    @admin.action(description='🟡 تنظیم وضعیت: بررسی‌شده')
    def set_status_reviewed(self, request, queryset):
        count = 0
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.status = 'reviewed'
                user.profile.save(update_fields=['status'])
                count += 1
        self.message_user(request, f'وضعیت {count} کاربر به «بررسی‌شده» تغییر کرد.')

    @admin.action(description='🟢 تنظیم وضعیت: خریده')
    def set_status_purchased(self, request, queryset):
        from django.utils import timezone
        count = 0
        for user in queryset:
            if hasattr(user, 'profile'):
                user.profile.status = 'purchased'
                if not user.profile.purchase_date:
                    user.profile.purchase_date = timezone.now().date()
                user.profile.save(update_fields=['status', 'purchase_date'])
                count += 1
        self.message_user(request, f'وضعیت {count} کاربر به «خریده» تغییر کرد و تاریخ خرید ثبت شد.')

    @admin.action(description='فعال‌سازی کاربران')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} کاربر فعال شدند.')

    @admin.action(description='غیرفعال‌سازی کاربران')
    def deactivate_users(self, request, queryset):
        updated = queryset.exclude(is_superuser=True).update(is_active=False)
        self.message_user(request, f'{updated} کاربر غیرفعال شدند.')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user_link',
        'phone',
        'job_class',
        'status_badge',
        'level_badge',
        'purchase_date',
        'referral_code',
        'referred_by_link',
        'is_agent',
        'created_at',
    )
    list_filter = (
        'status',
        'level',
        'created_at',
        'purchase_date',
    )
    search_fields = (
        'user__username', 'user__email', 'user__first_name', 'user__last_name',
        'referral_code', 'phone', 'job_class',
    )
    readonly_fields = ('referral_code', 'created_at', 'updated_at')
    raw_id_fields = ('referred_by',)
    list_per_page = 40
    list_editable = ('purchase_date', 'job_class')
    date_hierarchy = 'created_at'
    actions = [
        'mark_pending',
        'mark_reviewed',
        'mark_purchased',
    ]

    fieldsets = (
        ('کاربر', {
            'fields': ('user', 'referral_code', 'referred_by'),
        }),
        ('اطلاعات تماس و صنف', {
            'fields': ('phone', 'job_class', 'national_id', 'bank_card'),
        }),
        ('وضعیت و خرید', {
            'fields': ('status', 'purchase_date', 'admin_note'),
            'description': 'وضعیت: قرمز=بررسی‌نشده | زرد=بررسی‌شده | سبز=خریده',
        }),
        ('سطح و کیف پول', {
            'fields': ('level', 'points', 'total_sales', 'wallet_balance'),
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def user_link(self, obj):
        url = reverse('admin:auth_user_change', args=[obj.user.id])
        name = obj.user.get_full_name() or obj.user.username
        return format_html('<a href="{}">{}</a>', url, name)
    user_link.short_description = 'کاربر'
    user_link.admin_order_field = 'user__first_name'

    def status_badge(self, obj):
        colors = {
            'pending': ('#fef2f2', '#dc2626', '🔴 بررسی‌نشده'),
            'reviewed': ('#fefce8', '#ca8a04', '🟡 بررسی‌شده'),
            'purchased': ('#f0fdf4', '#16a34a', '🟢 خریده'),
        }
        bg, color, label = colors.get(obj.status, ('#f3f4f6', '#6b7280', obj.status))
        return format_html(
            '<span style="background:{}; color:{}; padding:4px 12px; border-radius:20px; '
            'font-size:12px; font-weight:700; display:inline-block; min-width:100px; text-align:center;">{}</span>',
            bg, color, label
        )
    status_badge.short_description = 'وضعیت'
    status_badge.admin_order_field = 'status'

    def level_badge(self, obj):
        colors = {'bronze': '#cd7f32', 'silver': '#a0a0a0', 'gold': '#ffd700'}
        labels = {'bronze': '🥉 برنزی', 'silver': '🥈 نقره‌ای', 'gold': '🥇 طلایی'}
        return format_html(
            '<span style="background:{}; color:#111; padding:3px 10px; border-radius:12px; font-size:12px; font-weight:bold;">{}</span>',
            colors.get(obj.level, '#999'), labels.get(obj.level, obj.level)
        )
    level_badge.short_description = 'سطح'

    def referred_by_link(self, obj):
        if obj.referred_by:
            return format_html(
                '{} <small style="color:#666;">({})</small>',
                obj.referred_by.user.get_full_name() or obj.referred_by.user.username,
                obj.referred_by.referral_code
            )
        return '—'
    referred_by_link.short_description = 'معرف'

    def is_agent(self, obj):
        has_refs = obj.referrals.exists()
        has_sales = obj.total_sales > 0
        if has_refs or has_sales:
            return format_html('<span style="color:#16a34a; font-weight:bold;">✓ عامل</span>')
        return format_html('<span style="color:#999;">کاربر عادی</span>')
    is_agent.short_description = 'نوع'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'referred_by', 'referred_by__user'
        ).annotate(ref_count=Count('referrals'))

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        qs = self.get_queryset(request)
        extra_context['status_counts'] = {
            'pending': qs.filter(status='pending').count(),
            'reviewed': qs.filter(status='reviewed').count(),
            'purchased': qs.filter(status='purchased').count(),
        }
        return super().changelist_view(request, extra_context=extra_context)

    @admin.action(description='🔴 علامت‌گذاری به عنوان بررسی‌نشده')
    def mark_pending(self, request, queryset):
        queryset.update(status='pending')
        self.message_user(request, f'{queryset.count()} مورد به بررسی‌نشده تغییر کرد.')

    @admin.action(description='🟡 علامت‌گذاری به عنوان بررسی‌شده')
    def mark_reviewed(self, request, queryset):
        queryset.update(status='reviewed')
        self.message_user(request, f'{queryset.count()} مورد به بررسی‌شده تغییر کرد.')

    @admin.action(description='🟢 علامت‌گذاری به عنوان خریده + ثبت تاریخ')
    def mark_purchased(self, request, queryset):
        from django.utils import timezone
        for p in queryset:
            p.status = 'purchased'
            if not p.purchase_date:
                p.purchase_date = timezone.now().date()
            p.save(update_fields=['status', 'purchase_date'])
        self.message_user(request, f'{queryset.count()} مورد به خریده تغییر کرد.')


# سفارشی‌سازی هدر ادمین
admin.site.site_header = 'پنل مدیریت افیلیت پرو'
admin.site.site_title = 'افیلیت پرو'
admin.site.index_title = 'داشبورد مدیریت'

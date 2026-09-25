from django.contrib import admin
from .models import ReferralClick


@admin.register(ReferralClick)
class ReferralClickAdmin(admin.ModelAdmin):
    list_display = ('referral_code', 'ip_address', 'created_at')
    search_fields = ('referral_code',)

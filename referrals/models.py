from django.db import models


class ReferralClick(models.Model):
    referral_code = models.CharField(max_length=12, verbose_name='کد معرف')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'کلیک معرف'
        verbose_name_plural = 'کلیک‌های معرف'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.referral_code} - {self.created_at}"

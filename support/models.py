from django.db import models
from django.contrib.auth.models import User
from products.models import Package


class SupportRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار'),
        ('approved', 'تأیید شده'),
        ('rejected', 'رد شده'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_requests', verbose_name='کاربر')
    package = models.ForeignKey(Package, on_delete=models.PROTECT, verbose_name='بسته')
    points_used = models.PositiveIntegerField(verbose_name='امتیاز مصرف شده')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    admin_note = models.TextField(blank=True, verbose_name='یادداشت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درخواست')
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'درخواست تمدید پشتیبانی'
        verbose_name_plural = 'درخواست‌های تمدید پشتیبانی'
        ordering = ['-created_at']

    def __str__(self):
        return f"پشتیبانی {self.user.username} - {self.package.name}"

from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):
    TYPE_CHOICES = (
        ('commission', 'کمیسیون'),
        ('purchase', 'خرید'),
        ('withdrawal', 'برداشت'),
        ('support', 'تمدید پشتیبانی'),
        ('bonus', 'پاداش'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', verbose_name='کاربر')
    amount = models.IntegerField(verbose_name='مبلغ')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='نوع')
    description = models.CharField(max_length=255, blank=True, verbose_name='توضیحات')
    balance_after = models.PositiveIntegerField(default=0, verbose_name='موجودی بعد از تراکنش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ')

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_type_display()} - {self.amount:,}"


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = (
        ('unread', 'خوانده‌نشده'),
        ('read', 'خوانده‌شده'),
        ('approved', 'تأیید شده'),
        ('rejected', 'رد شده'),
        ('paid', 'پرداخت شده'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawals', verbose_name='کاربر')
    amount = models.PositiveIntegerField(verbose_name='مبلغ درخواستی')
    bank_card = models.CharField(max_length=16, verbose_name='شماره کارت')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread', verbose_name='وضعیت')
    admin_note = models.TextField(blank=True, verbose_name='یادداشت ادمین')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درخواست')
    processed_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پردازش')
    is_seen = models.BooleanField(default=False, verbose_name='مشاهده شده')

    class Meta:
        verbose_name = 'درخواست برداشت'
        verbose_name_plural = 'درخواست‌های برداشت'
        ordering = ['-created_at']

    def __str__(self):
        return f"برداشت {self.amount:,} - {self.user.username} ({self.get_status_display()})"

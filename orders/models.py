from django.db import models
from django.contrib.auth.models import User
from products.models import Package


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('cancelled', 'لغو شده'),
        ('refunded', 'عودت داده شده'),
    )

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='خریدار')
    package = models.ForeignKey(Package, on_delete=models.PROTECT, verbose_name='بسته')
    amount = models.PositiveIntegerField(verbose_name='مبلغ')
    referrer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='referred_orders', verbose_name='معرف'
    )
    commission_amount = models.PositiveIntegerField(default=0, verbose_name='مبلغ کمیسیون')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    tracking_code = models.CharField(max_length=20, unique=True, blank=True, verbose_name='کد پیگیری')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='زمان پرداخت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    notes = models.TextField(blank=True, verbose_name='یادداشت')

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارشات'
        ordering = ['-created_at']

    def __str__(self):
        return f"سفارش #{self.id} - {self.buyer.username} - {self.package.name}"

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            import random
            import string
            self.tracking_code = 'ORD-' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    def mark_as_paid(self):
        from django.utils import timezone
        if self.status == 'paid':
            return
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.save()
        if hasattr(self.buyer, 'profile'):
            self.buyer.profile.points += self.package.points_reward
            self.buyer.profile.save(update_fields=['points'])
        if self.referrer and hasattr(self.referrer, 'profile'):
            commission = self.referrer.profile.add_commission(self.amount)
            self.commission_amount = commission
            self.save(update_fields=['commission_amount'])

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string


def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class UserProfile(models.Model):
    LEVEL_CHOICES = (
        ('bronze', 'برنزی'),
        ('silver', 'نقره‌ای'),
        ('gold', 'طلایی'),
    )

    STATUS_CHOICES = (
        ('pending', 'بررسی‌نشده'),
        ('reviewed', 'بررسی‌شده'),
        ('purchased', 'خریده'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='کاربر')
    referral_code = models.CharField(max_length=12, unique=True, default=generate_referral_code, verbose_name='کد معرف')
    referred_by = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='referrals', verbose_name='معرف'
    )
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='bronze', verbose_name='سطح')
    points = models.PositiveIntegerField(default=0, verbose_name='امتیاز')
    total_sales = models.PositiveIntegerField(default=0, verbose_name='تعداد فروش')
    wallet_balance = models.PositiveIntegerField(default=0, verbose_name='موجودی کیف پول (تومان)')
    phone = models.CharField(max_length=15, blank=True, verbose_name='شماره موبایل')
    national_id = models.CharField(max_length=10, blank=True, verbose_name='کد ملی')
    bank_card = models.CharField(max_length=16, blank=True, verbose_name='شماره کارت')
    job_class = models.CharField(max_length=100, blank=True, verbose_name='صنف کاری')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='وضعیت بررسی',
        db_index=True,
    )
    purchase_date = models.DateField(null=True, blank=True, verbose_name='تاریخ خرید')
    admin_note = models.TextField(blank=True, verbose_name='یادداشت ادمین')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ عضویت')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_level_display()}"

    @property
    def commission_rate(self):
        rates = {'bronze': 5, 'silver': 10, 'gold': 12}
        return rates.get(self.level, 5)

    @property
    def next_level_sales(self):
        if self.level == 'bronze':
            return max(0, 10 - self.total_sales)
        elif self.level == 'silver':
            return max(0, 20 - self.total_sales)
        return 0

    @property
    def progress_percent(self):
        if self.level == 'bronze':
            return min(100, int((self.total_sales / 10) * 100))
        elif self.level == 'silver':
            return min(100, int((self.total_sales / 20) * 100))
        return 100

    @property
    def can_withdraw(self):
        return self.level == 'gold'

    def check_level_up(self):
        if self.level == 'bronze' and self.total_sales >= 10:
            self.level = 'silver'
            self.save(update_fields=['level'])
            return 'silver'
        elif self.level == 'silver' and self.total_sales >= 20:
            self.level = 'gold'
            self.save(update_fields=['level'])
            return 'gold'
        return None

    def add_commission(self, amount):
        commission = int(amount * self.commission_rate / 100)
        self.points += commission
        self.wallet_balance += commission
        self.total_sales += 1
        self.save()
        self.check_level_up()
        return commission

    def status_color(self):
        return {
            'pending': '#ef4444',    # قرمز
            'reviewed': '#eab308',   # زرد
            'purchased': '#22c55e',  # سبز
        }.get(self.status, '#999')

    def status_label(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

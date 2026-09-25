from django.db import models


class Package(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام بسته')
    slug = models.SlugField(unique=True, verbose_name='اسلاگ')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    price = models.PositiveIntegerField(verbose_name='قیمت (تومان)')
    support_price = models.PositiveIntegerField(default=0, verbose_name='قیمت تمدید پشتیبانی (تومان)')
    duration_days = models.PositiveIntegerField(default=30, verbose_name='مدت پشتیبانی (روز)')
    points_reward = models.PositiveIntegerField(default=0, verbose_name='امتیاز هدیه به خریدار')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    display_order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    image = models.ImageField(upload_to='packages/', blank=True, null=True, verbose_name='تصویر')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'بسته'
        verbose_name_plural = 'بسته‌ها'
        ordering = ['display_order', 'price']

    def __str__(self):
        return f"{self.name} - {self.price:,} تومان"

    @property
    def price_formatted(self):
        return f"{self.price:,}"

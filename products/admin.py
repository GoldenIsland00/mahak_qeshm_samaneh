from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from django import forms
from .models import Package


class BulkPriceForm(forms.Form):
    MODE_CHOICES = (
        ('percent', 'افزایش درصدی (%)'),
        ('fixed', 'افزایش مبلغ ثابت (تومان)'),
    )
    mode = forms.ChoiceField(choices=MODE_CHOICES, label='نوع افزایش', widget=forms.RadioSelect)
    value = forms.IntegerField(min_value=1, label='مقدار', help_text='مثلاً ۱۰ برای ۱۰٪ یا ۵۰۰۰۰ برای ۵۰ هزار تومان')
    apply_to_support = forms.BooleanField(required=False, initial=True, label='روی قیمت پشتیبانی هم اعمال شود')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_display', 'support_price_display', 'duration_days', 'is_active', 'is_featured', 'display_order')
    list_filter = ('is_active', 'is_featured')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_featured', 'display_order')
    actions = ['bulk_increase_price']
    change_list_template = 'admin/products/package_changelist.html'

    def price_display(self, obj):
        return f"{obj.price:,} تومان"
    price_display.short_description = 'قیمت'

    def support_price_display(self, obj):
        return f"{obj.support_price:,}"
    support_price_display.short_description = 'قیمت پشتیبانی'

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('bulk-price/', self.admin_site.admin_view(self.bulk_price_view), name='products_package_bulk_price'),
        ]
        return custom + urls

    def bulk_price_view(self, request):
        if request.method == 'POST':
            form = BulkPriceForm(request.POST)
            if form.is_valid():
                mode = form.cleaned_data['mode']
                value = form.cleaned_data['value']
                apply_support = form.cleaned_data['apply_to_support']
                packages = Package.objects.all()
                count = 0
                for p in packages:
                    if mode == 'percent':
                        p.price = int(p.price * (1 + value / 100))
                        if apply_support:
                            p.support_price = int(p.support_price * (1 + value / 100))
                    else:
                        p.price = p.price + value
                        if apply_support:
                            p.support_price = p.support_price + value
                    p.save()
                    count += 1
                messages.success(request, f'قیمت {count} بسته با موفقیت به‌روز شد.')
                return redirect('admin:products_package_changelist')
        else:
            form = BulkPriceForm()
        context = {
            **self.admin_site.each_context(request),
            'form': form,
            'title': 'افزایش دسته‌ای قیمت بسته‌ها',
            'opts': self.model._meta,
        }
        return render(request, 'admin/products/bulk_price.html', context)

    @admin.action(description='افزایش قیمت انتخاب‌شده‌ها (از منوی اقدامات استفاده کنید یا دکمه بالا)')
    def bulk_increase_price(self, request, queryset):
        return redirect('admin:products_package_bulk_price')

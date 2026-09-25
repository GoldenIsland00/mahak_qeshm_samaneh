from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='job_class',
            field=models.CharField(blank=True, max_length=100, verbose_name='صنف کاری'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.CharField(
                choices=[('pending', 'بررسی‌نشده'), ('reviewed', 'بررسی‌شده'), ('purchased', 'خریده')],
                db_index=True,
                default='pending',
                max_length=20,
                verbose_name='وضعیت بررسی',
            ),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='purchase_date',
            field=models.DateField(blank=True, null=True, verbose_name='تاریخ خرید'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='admin_note',
            field=models.TextField(blank=True, verbose_name='یادداشت ادمین'),
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'پروفایل کاربر',
                'verbose_name_plural': 'پروفایل کاربران',
            },
        ),
    ]

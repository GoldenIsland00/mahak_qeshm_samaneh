from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawalrequest',
            name='is_seen',
            field=models.BooleanField(default=False, verbose_name='مشاهده شده'),
        ),
        migrations.AlterField(
            model_name='withdrawalrequest',
            name='status',
            field=models.CharField(
                choices=[
                    ('unread', 'خوانده‌نشده'),
                    ('read', 'خوانده‌شده'),
                    ('approved', 'تأیید شده'),
                    ('rejected', 'رد شده'),
                    ('paid', 'پرداخت شده'),
                ],
                default='unread',
                max_length=20,
                verbose_name='وضعیت',
            ),
        ),
    ]

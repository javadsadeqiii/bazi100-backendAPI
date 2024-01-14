# Generated by Django 5.0 on 2024-01-14 14:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_customuser_downloadtype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='lastRechargeDate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ آخرین آپدیت دانلودها'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='remainingDays',
            field=models.IntegerField(default=30, verbose_name='روز باقی\u200cمانده'),
        ),
        migrations.AlterField(
            model_name='albums',
            name='zipFile',
            field=models.CharField(verbose_name='فایل زیپ'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='soundtrackDownloads',
            field=models.IntegerField(default=100, verbose_name='soundtrack_dl_remain'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='wallpaperDownloads',
            field=models.IntegerField(default=100, verbose_name='wallpaper_dl_remain'),
        ),
        migrations.AlterField(
            model_name='tracks',
            name='audioFile',
            field=models.CharField(verbose_name='فایل موسیقی'),
        ),
        migrations.AlterField(
            model_name='wallpapers',
            name='image',
            field=models.CharField(null=True, verbose_name='فایل والپیپر'),
        ),
    ]

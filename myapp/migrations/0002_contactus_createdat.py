# Generated by Django 5.0 on 2024-01-08 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='createdAt',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان و تاریخ '),
        ),
    ]

# Generated by Django 5.0 on 2023-12-25 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_subscriber_delete_newsletter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriber',
            options={'verbose_name': 'خبرنامه', 'verbose_name_plural': 'خبرنامه'},
        ),
    ]
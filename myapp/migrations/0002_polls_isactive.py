# Generated by Django 5.0 on 2023-12-17 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='polls',
            name='isActive',
            field=models.BooleanField(default=False, null=True),
        ),
    ]

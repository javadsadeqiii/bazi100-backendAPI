# Generated by Django 5.0 on 2023-12-19 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_reply_parentreplyid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='parentReplyId',
            field=models.ForeignKey(blank=True, default=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='myapp.reply', verbose_name='ریپلای والد'),
        ),
    ]
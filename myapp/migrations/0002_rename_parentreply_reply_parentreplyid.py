# Generated by Django 5.0 on 2023-12-23 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='parentReply',
            new_name='parentReplyId',
        ),
    ]

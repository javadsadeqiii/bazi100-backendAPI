# Generated by Django 5.0 on 2023-12-20 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allposts',
            name='relatedComments',
        ),
    ]
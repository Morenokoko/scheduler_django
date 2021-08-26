# Generated by Django 3.2.6 on 2021-08-25 19:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0016_auto_20210826_0312'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together={('user', 'date', 'rank'), ('user', 'date', 'shift')},
        ),
    ]
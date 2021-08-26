# Generated by Django 3.2.6 on 2021-08-24 21:48

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0004_availability_shift'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availability',
            old_name='employee',
            new_name='user',
        ),
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together={('user', 'date', 'shift')},
        ),
    ]

# Generated by Django 3.2.6 on 2021-08-25 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20210825_1848'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together={('date', 'shift')},
        ),
    ]
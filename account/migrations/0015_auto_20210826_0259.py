# Generated by Django 3.2.6 on 2021-08-25 18:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_schedule_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='time',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
        migrations.AlterUniqueTogether(
            name='shift',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='shift',
            name='shiftendtime',
        ),
        migrations.RemoveField(
            model_name='shift',
            name='shiftstarttime',
        ),
    ]

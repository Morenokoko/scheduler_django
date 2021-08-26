# Generated by Django 3.2.6 on 2021-08-24 23:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0009_alter_availability_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('shift1employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Shift_1', to=settings.AUTH_USER_MODEL)),
                ('shift2employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Shift_2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
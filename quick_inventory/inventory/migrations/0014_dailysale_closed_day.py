# Generated by Django 5.0.3 on 2024-12-04 17:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_remove_dailysale_closed_day_dailysale_is_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailysale',
            name='closed_day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.closedday'),
        ),
    ]

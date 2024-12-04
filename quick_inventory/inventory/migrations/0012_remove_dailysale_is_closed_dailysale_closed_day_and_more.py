# Generated by Django 5.0.3 on 2024-12-04 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_remove_dailysale_closed_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailysale',
            name='is_closed',
        ),
        migrations.AddField(
            model_name='dailysale',
            name='closed_day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.closedday'),
        ),
        migrations.AlterField(
            model_name='dailysale',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
    ]

# Generated by Django 5.0.3 on 2024-12-04 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_remove_dailysale_is_closed_dailysale_closed_day_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailysale',
            name='closed_day',
        ),
        migrations.AddField(
            model_name='dailysale',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]

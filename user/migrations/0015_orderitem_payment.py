# Generated by Django 5.1.5 on 2025-02-04 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_orderitem_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='payment',
            field=models.BooleanField(default=False, help_text='0-NotPaid, 1-Paid'),
        ),
    ]

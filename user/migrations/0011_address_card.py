# Generated by Django 5.1.5 on 2025-02-03 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_useramount'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='card',
            field=models.IntegerField(default=0),
        ),
    ]

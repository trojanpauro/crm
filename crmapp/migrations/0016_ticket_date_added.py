# Generated by Django 2.2.6 on 2023-05-08 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0015_auto_20230508_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

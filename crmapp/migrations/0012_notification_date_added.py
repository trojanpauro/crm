# Generated by Django 2.2.6 on 2023-05-07 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0011_conversation_session_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

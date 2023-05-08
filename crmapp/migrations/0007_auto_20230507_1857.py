# Generated by Django 2.2.6 on 2023-05-07 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0006_message_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='status',
            field=models.CharField(choices=[('sent', 'sent'), ('read', 'read'), ('replied', 'replied')], default='sent', max_length=50),
        ),
    ]

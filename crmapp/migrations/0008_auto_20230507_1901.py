# Generated by Django 2.2.6 on 2023-05-07 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0007_auto_20230507_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='message_to', to='crmapp.Persona'),
        ),
    ]

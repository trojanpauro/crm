# Generated by Django 2.2.6 on 2023-05-07 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0010_agent_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='session_key',
            field=models.CharField(default='HHS', max_length=200),
            preserve_default=False,
        ),
    ]

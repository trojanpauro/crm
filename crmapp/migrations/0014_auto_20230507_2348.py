# Generated by Django 2.2.6 on 2023-05-07 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0013_auto_20230507_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='conversation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='crmapp.Conversation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='lead',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='crmapp.Lead'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='ticket',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='crmapp.Ticket'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='agents',
            field=models.ManyToManyField(to='crmapp.Agent'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='tittle',
            field=models.CharField(default='1', max_length=20),
            preserve_default=False,
        ),
    ]

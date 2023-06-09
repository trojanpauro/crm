# Generated by Django 2.2.6 on 2023-05-14 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crmapp', '0019_auto_20230508_0443'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversation',
            old_name='customer',
            new_name='conversation_customer',
        ),
        migrations.RenameField(
            model_name='lead',
            old_name='customer',
            new_name='lead_customer',
        ),
        migrations.RenameField(
            model_name='sale',
            old_name='customer',
            new_name='sale_customer',
        ),
        migrations.RenameField(
            model_name='subscriptions',
            old_name='customer',
            new_name='subscription_customer',
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_customer',
            field=models.ForeignKey(default='3', on_delete=django.db.models.deletion.PROTECT, to='crmapp.Customer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='category',
            field=models.CharField(choices=[('first_contact', 'first contact'), ('multiple_contact', 'multiple contact'), ('purchased', 'purchased'), ('unsubscribed', 'unsubscribed')], max_length=100),
        ),
        migrations.AlterField(
            model_name='lead',
            name='state',
            field=models.CharField(choices=[('prospect', 'prospect'), ('qualified_lead', 'qualified_lead'), ('pitch', 'pitch'), ('closing', 'closing'), ('nurturing', 'nurturing')], max_length=30),
        ),
    ]

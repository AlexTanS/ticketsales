# Generated by Django 4.2.11 on 2024-12-31 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_services_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='services',
            name='service',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='services',
        ),
        migrations.AddField(
            model_name='listofservices',
            name='service',
            field=models.ForeignKey(help_text='номер заказа', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.services', verbose_name='заказ'),
        ),
        migrations.AddField(
            model_name='services',
            name='ticket',
            field=models.ForeignKey(blank=True, default=None, help_text='билет к которому принадлежит заказ', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.ticket', verbose_name='билет'),
        ),
    ]

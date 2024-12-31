# Generated by Django 4.2.11 on 2024-12-30 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bus',
            options={'verbose_name': 'автобус', 'verbose_name_plural': 'автобусы'},
        ),
        migrations.AlterModelOptions(
            name='finishcity',
            options={'verbose_name': 'город назначения', 'verbose_name_plural': 'города назначения'},
        ),
        migrations.AlterModelOptions(
            name='listofservices',
            options={'ordering': ['name'], 'verbose_name': 'услуги', 'verbose_name_plural': 'услуги'},
        ),
        migrations.AlterModelOptions(
            name='services',
            options={'verbose_name': 'заказанная услуга', 'verbose_name_plural': 'заказанные услуги'},
        ),
        migrations.AlterModelOptions(
            name='startcity',
            options={'verbose_name': 'город отправления', 'verbose_name_plural': 'города отправления'},
        ),
        migrations.AlterField(
            model_name='services',
            name='service',
            field=models.ManyToManyField(default=None, help_text='заказанные услуги', to='app.listofservices', verbose_name='услуги'),
        ),
    ]
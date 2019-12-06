# Generated by Django 2.2.7 on 2019-12-05 20:53

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0006_auto_20191205_2051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conseil',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 5, 20, 53, 55, 850447, tzinfo=utc), help_text='date de fin du conseil.', verbose_name='date de fin du conseil'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 5, 20, 53, 55, 848523, tzinfo=utc), help_text='date de fin du contrat.', verbose_name='date de fin du contrat'),
        ),
        migrations.AlterField(
            model_name='license',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2020, 1, 5, 20, 53, 55, 851822, tzinfo=utc), help_text='durée de la license (en mois/jours).', verbose_name='durée de la license'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Account Manager'), (1, 'Manager General'), (3, 'Factu Manager')], default=3, help_text='préciser son rôle.', verbose_name='rôle du manager.'),
        ),
    ]

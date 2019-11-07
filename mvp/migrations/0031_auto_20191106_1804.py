# Generated by Django 2.2.7 on 2019-11-06 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0030_auto_20191106_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(4, 'Commercial'), (2, 'STAFF'), (1, 'DEV'), (3, 'CEO')], default=4, unique=True, verbose_name='user type'),
        ),
    ]

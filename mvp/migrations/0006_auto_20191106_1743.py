# Generated by Django 2.2.7 on 2019-11-06 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0005_auto_20191106_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(3, 'CEO'), (4, 'Commercial'), (1, 'DEV'), (2, 'STAFF')], default=4, unique=True, verbose_name='user type'),
        ),
    ]

# Generated by Django 2.2.7 on 2019-11-07 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0043_auto_20191107_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(3, 'CEO'), (4, 'Commercial'), (2, 'STAFF'), (1, 'DEV')], default=4, verbose_name='user type'),
        ),
    ]

# Generated by Django 2.2.7 on 2019-12-14 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0017_auto_20191213_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Account Manager'), (3, 'Factu Manager'), (1, 'Manager General')], default=3, help_text='préciser le rôle du manager.', verbose_name='rôle du manager.'),
        ),
        migrations.AlterField(
            model_name='service',
            name='done',
            field=models.SmallIntegerField(choices=[(2, 'Ne sera jamais effectué'), (0, 'Pas encore effectué'), (1, 'Effectué')], default=0, help_text='précisez si le service est effectué.', verbose_name='si le service est effectué.'),
        ),
    ]
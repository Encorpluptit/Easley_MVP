# Generated by Django 2.2.7 on 2019-12-18 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0029_auto_20191218_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Responsable Facturation'), (2, 'Responsable Clientèle'), (4, 'Commercial'), (1, 'Manager')], default=4, help_text='Préciser le rôle de la personne', verbose_name='Rôle de la personne'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Factu Manager'), (1, 'Manager General'), (2, 'Account Manager')], default=3, help_text='préciser le rôle du manager.', verbose_name='rôle du manager.'),
        ),
        migrations.AlterField(
            model_name='service',
            name='done',
            field=models.SmallIntegerField(choices=[(2, 'Ne sera jamais effectué'), (0, 'Pas encore effectué'), (1, 'Effectué')], default=0, help_text='Précisez si le service est effectué.', verbose_name='Si le service est effectué.'),
        ),
    ]

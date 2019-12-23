# Generated by Django 2.2.7 on 2019-12-19 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0034_auto_20191218_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Manager'), (2, 'Responsable Clientèle'), (4, 'Commercial'), (3, 'Responsable Facturation')], default=4, help_text='Préciser le rôle de la personne', verbose_name='Rôle de la personne'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Manager General'), (2, 'Account Manager'), (3, 'Factu Manager')], default=3, help_text='préciser le rôle du manager.', verbose_name='rôle du manager.'),
        ),
        migrations.AlterField(
            model_name='service',
            name='done',
            field=models.SmallIntegerField(choices=[(0, 'Pas encore effectué'), (2, 'Ne sera jamais effectué'), (1, 'Effectué')], default=0, help_text='Précisez si le service est effectué.', verbose_name='Si le service est effectué.'),
        ),
    ]
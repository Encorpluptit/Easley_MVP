# Generated by Django 2.2.7 on 2020-01-09 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0002_auto_20200109_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='facturation_delay',
            field=models.PositiveSmallIntegerField(choices=[(60, '60 Jours'), (30, '30 Jours'), (45, '45 Jours'), (15, '15 Jours'), (75, '75 Jours'), (90, '90 Jours')], default=45, help_text='Précisez le délai à partir duquel un client est considéré en retard de paiement.', verbose_name='Délai de facturation.'),
        ),
        migrations.AlterField(
            model_name='invite',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Manager'), (3, 'Responsable Facturation'), (4, 'Commercial'), (2, 'Responsable Clientèle')], default=4, help_text='Préciser le rôle de la personne', verbose_name='Rôle de la personne'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Factu Manager'), (1, 'Manager General'), (2, 'Account Manager')], default=3, help_text='préciser le rôle du manager.', verbose_name='rôle du manager.'),
        ),
        migrations.AlterField(
            model_name='service',
            name='done',
            field=models.SmallIntegerField(choices=[(2, 'Ne sera jamais effectué'), (1, 'Effectué'), (0, 'Pas encore effectué')], default=0, help_text='Précisez si le service est effectué.', verbose_name='Si le service est effectué.'),
        ),
    ]

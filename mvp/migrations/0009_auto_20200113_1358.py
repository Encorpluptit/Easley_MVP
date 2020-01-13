# Generated by Django 2.2.7 on 2020-01-13 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvp', '0008_auto_20200113_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(default=None, help_text="L'email du destinataire.", max_length=150, verbose_name='Email du destinataire.')),
            ],
            options={
                'verbose_name': 'email database',
                'verbose_name_plural': 'emails database',
                'ordering': ['email'],
            },
        ),
        migrations.AlterField(
            model_name='company',
            name='facturation_delay',
            field=models.PositiveSmallIntegerField(choices=[(90, '90 Jours'), (75, '75 Jours'), (30, '30 Jours'), (60, '60 Jours'), (15, '15 Jours'), (45, '45 Jours')], default=45, help_text='Précisez le délai à partir duquel un client est considéré en retard de paiement.', verbose_name='Délai de facturation.'),
        ),
        migrations.AlterField(
            model_name='invite',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Responsable Facturation'), (1, 'Manager'), (4, 'Commercial'), (2, 'Responsable Clientèle')], default=4, help_text='Préciser le rôle de la personne', verbose_name='Rôle de la personne'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(2, 'Account Manager'), (1, 'Manager General'), (3, 'Factu Manager')], default=3, help_text='préciser le rôle du manager.', verbose_name='rôle du manager.'),
        ),
        migrations.AlterField(
            model_name='service',
            name='done',
            field=models.SmallIntegerField(choices=[(1, 'Effectué'), (2, 'Ne sera jamais effectué'), (0, 'Pas encore effectué')], default=0, help_text='Précisez si le service est effectué.', verbose_name='Si le service est effectué.'),
        ),
    ]

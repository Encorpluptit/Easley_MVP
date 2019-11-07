# Generated by Django 2.2.7 on 2019-11-06 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mvp', '0019_auto_20191106_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='companies',
            name='ceo',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL, verbose_name="company's ceo"),
        ),
        migrations.AlterField(
            model_name='profile',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(3, 'CEO'), (2, 'STAFF'), (1, 'DEV'), (4, 'Commercial')], default=4, unique=True, verbose_name='user type'),
        ),
    ]

# Generated by Django 3.2 on 2021-04-27 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_plasmadonor'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodrequest',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In-touch', 'In-touch'), ('Inappropriate', 'Inappropriate'), ('Insufficient', 'Insufficient'), ('Fulfilled', 'Fulfilled')], default='Pending', max_length=15),
        ),
    ]

# Generated by Django 3.2 on 2021-05-08 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_careerpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='careerpost',
            name='nature',
            field=models.CharField(choices=[('Work from home', 'Work form home')], default='Work form home', max_length=15),
            preserve_default=False,
        ),
    ]
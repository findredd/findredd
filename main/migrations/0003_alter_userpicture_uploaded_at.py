# Generated by Django 3.2 on 2021-04-12 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_bloodrequest_districtcoordinator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpicture',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

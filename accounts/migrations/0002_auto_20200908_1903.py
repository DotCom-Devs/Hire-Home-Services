# Generated by Django 3.1.1 on 2020-09-08 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lastupdated',
            name='update_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]

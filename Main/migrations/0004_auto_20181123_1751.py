# Generated by Django 2.1.3 on 2018-11-23 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_auto_20181123_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='end',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='start',
            field=models.TimeField(),
        ),
    ]

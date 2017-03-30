# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 02:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherApp', '0005_auto_20170328_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='retrieved',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='api_ref_string',
            field=models.CharField(db_index=True, max_length=200),
        ),
    ]
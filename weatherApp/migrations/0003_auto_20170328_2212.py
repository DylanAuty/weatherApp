# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-28 22:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherApp', '0002_auto_20170322_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conditions',
            name='dewpoint',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='feelslike',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='humidity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='precip_1hr',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='precip_today',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='pressure',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='temperature',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='uv',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='visibility',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='windspeed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conditions',
            name='windspeed_gust',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='ave_humidity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='ave_windspeed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='high',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='low',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='max_humidity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='max_windspeed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='min_humidity',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='pop',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='pop_tf_day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='pop_tf_night',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]

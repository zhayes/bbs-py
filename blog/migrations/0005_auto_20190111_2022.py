# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-01-11 20:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_expression'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.IntegerField(default=1),
        ),
    ]
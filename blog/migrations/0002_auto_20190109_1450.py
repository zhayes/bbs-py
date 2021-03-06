# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2019-01-09 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('publish_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment_count', models.IntegerField(default=0)),
                ('content', models.TextField(max_length=30000)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('comment', models.CharField(max_length=500)),
                ('article_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=32)),
                ('avatar', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ['create_time'],
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_id', to='blog.Comment'),
        ),
        migrations.AddField(
            model_name='article',
            name='author_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to='blog.User'),
        ),
        migrations.AddField(
            model_name='article',
            name='author_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_name', to='blog.User'),
        ),
    ]

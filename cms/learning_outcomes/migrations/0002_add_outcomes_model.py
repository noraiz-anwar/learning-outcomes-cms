# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-04-10 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_outcomes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Outcomes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.CharField(max_length=100, unique=True)),
                ('prerequisites', models.ManyToManyField(blank=True, to='learning_outcomes.Outcomes')),
            ],
        ),
        migrations.RemoveField(
            model_name='topic',
            name='prerequisites',
        ),
        migrations.AddField(
            model_name='topic',
            name='outcomes',
            field=models.ManyToManyField(blank=True, to='learning_outcomes.Outcomes'),
        ),
    ]
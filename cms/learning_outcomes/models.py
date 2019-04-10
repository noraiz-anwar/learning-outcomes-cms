# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Outcomes(models.Model):
    statement = models.CharField(max_length=100, unique=True)
    prerequisites = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.statement


class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, default='')
    outcomes = models.ManyToManyField("Outcomes", blank=True)
    
    def __str__(self):
        return self.name


class TopicStructure(MPTTModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_topics')

    class MPTTMeta:
        order_insertion_by = ['topic']
    
    def __str__(self):
        return self.topic.name


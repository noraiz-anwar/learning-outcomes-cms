# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey


class Outcomes(models.Model):
    statement = models.CharField(max_length=100, unique=True)
    prerequisites = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.statement


class Topic(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, default='', blank=True)
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


@receiver(post_save, sender=TopicStructure)
def remove_outcomes(sender, **kwargs):
    instance = kwargs.get('instance', None)
    parent_outcomes = []
    if instance.parent:
        parent_outcomes_qs = instance.parent.topic.outcomes.all()
        for outcome in parent_outcomes_qs:
            parent_outcomes.append(outcome)
            instance.parent.topic.outcomes.remove(outcome)
    else:
        return

    if parent_outcomes:
        leaf_node = []

        parents = [instance.topic]
        while parents:
            parent = parents.pop()
            parent = TopicStructure.objects.get(topic=parent)
            if parent.is_leaf_node():
                leaf_node.append(parent)
            else:
                children = TopicStructure.objects.filter(parent=parent)
                for node in children:
                    parents.append(node.topic)

        for node in leaf_node:
            topic = node.topic
            for outcome in parent_outcomes:
                topic.outcomes.add(outcome)

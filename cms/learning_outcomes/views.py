# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.http import HttpResponse
from models import TopicStructure


def index(request):
    context = {'nodes': TopicStructure.objects.all()}
    return render(request, 'index.html', context)

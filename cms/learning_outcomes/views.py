# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import TopicStructure


def index(request):
    context = {'nodes': TopicStructure.objects.all()}
    return render(request, 'index.html', context)


class AddTopicStructure(TemplateView):
    template_name = "admin/upload.html"

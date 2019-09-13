# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import io

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from .models import Topic
from .models import TopicStructure
from .utils import generate_tree


def index(request):
    context = {'nodes': TopicStructure.objects.all()}
    return render(request, 'index.html', context)


class AddTopicStructure(TemplateView):
    template_name = "admin/upload.html"

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AddTopicStructure, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.FILES['myfile']:
            data = request.POST.copy()
            levels = 0
            parent_name = data.get('parentName')
            csv_file = io.TextIOWrapper(request.FILES['myfile'].file)
            csv_reader = csv.reader(csv_file, delimiter=',')
            headings = next(csv_reader)

            # Determine the topic hierarchy levels
            for heading in headings:
                if heading.lower() in ["topic", "topics"]:
                    levels += 1

            parent_topic = Topic.objects.get_or_create(name=parent_name)
            parent_topic_structure = TopicStructure.objects.get_or_create(topic=parent_topic[0],
                                                                          parent=None)
            generate_tree(levels, csv_reader, parent_topic_structure[0])

            context = super(AddTopicStructure, self).get_context_data(**kwargs)
            context['done'] = "Your topic Structure with parent :" + parent_name + ", is now updated"
        return render(request, self.template_name, context)

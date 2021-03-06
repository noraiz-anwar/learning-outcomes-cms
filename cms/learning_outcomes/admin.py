# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import DraggableMPTTAdmin

from .forms import TopicForm
from .models import Topic, TopicStructure, Outcomes


class MyDraggableMPTTAdmin(DraggableMPTTAdmin):
    list_per_page = 100
    list_display = ('tree_actions', 'title')
    list_display_links = ('title',)

    def title(self, instance):
        return format_html(
            '<div style="text-indent:">{}-{}</div>',
             '---' * (instance._mpttfield('level')),
            instance.topic,
        )
    title.short_description = 'Name'


class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']
    form = TopicForm


class OutcomesAdmin(admin.ModelAdmin):
    pass


admin.site.register(
    TopicStructure,
    MyDraggableMPTTAdmin,
    search_fields=['topic__name']
)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Outcomes, OutcomesAdmin)


# Customization
admin.site.site_header = 'Course Management System'
admin.site.site_title = 'CMS'
admin.site.index_title = ''

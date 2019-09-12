from django.conf.urls import url
from django.contrib import admin

from .views import index, AddTopicStructure

urlpatterns = [
    url(r'^learning_outcomes_tree/$', index, name='index'),
    url(r'^', admin.site.urls),
    url(r'add_topic_structure/$', AddTopicStructure.as_view(), name='add_topic_structure'),
]

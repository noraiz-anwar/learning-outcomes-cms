from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Topic, TopicStructure


class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'category', 'outcomes', ]

    def clean(self):
        cleaned_data = super(TopicForm, self).clean()
        outcomes = cleaned_data['outcomes']
        is_parent = TopicStructure.objects.filter(parent__topic=self.instance)
        if outcomes and is_parent:
            raise ValidationError("Outcome can only be associated with the leaf node. This is not a leaf node")
        return cleaned_data

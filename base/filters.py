import django_filters
from django_filters import CharFilter
from django.forms.widgets import TextInput

from django import forms 

from .models import *

class PostFilter(django_filters.FilterSet):
    headline = CharFilter(field_name='headline', lookup_expr="icontains", label='', widget=TextInput(attrs={'placeholder': 'Search here...'}))
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple, label='Search by Tags:'
    )
    class Meta:
        model = Post
        fields = ['headline', 'tags']
        



from django.forms import ModelForm
from .models import Pin, Board, Topic
from django import forms

class PinForm(ModelForm):
    class Meta:
        model = Pin
        fields = ['title', 'description', 'image', 'topic']

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'description', 'topic']

class TopicForm(ModelForm):
    class Meta:
        model = Topic
        fields = ['name']
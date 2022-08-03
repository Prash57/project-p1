from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Post, Comment, Tag, Image


class PostForm(ModelForm):

    class Meta:
        model = Post
        # fields = ['headline', 'sub_headline', 'thumbnail', 'body', 'tags']
        fields = '__all__'


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'


class AddTagsForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']

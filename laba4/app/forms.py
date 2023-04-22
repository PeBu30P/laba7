"""
Definition of forms.
"""

from mimetypes import init
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Comment, Blog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class FeedbackForm(forms.Form):
    username = forms.CharField(label='Ваше имя', min_length=2, max_length=100)
    gender = forms.ChoiceField(
        label='Ваш пол',
        choices=[('1', 'Мужской'), ('2', 'Женский')],
        widget=forms.RadioSelect(),
        initial=1,
    )
    corn = forms.BooleanField(label='Я козерог', required=False)
    rate = forms.ChoiceField(
        label='Ваша оценка сайта',
        choices=(('1', 'плохо'), ('2', 'нормально'), ('3', 'отлично')),
        initial=3,
    )
    feedback = forms.CharField(
        required=False,
        label='Ваш отзыв',
        widget=forms.Textarea(attrs={'rows': '10', 'cols': '70'}),
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        labels = {"text": ""}
        widgets = {"text": forms.Textarea(attrs={"class": "form-control"})}


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = (
            "title",
            "descripstion",
            "content",
            "image",
        )
        labels = {
            "title": "Заголовок",
            "descripstion": "Краткое содержание",
            "content": "Полное содержание",
            "image": "Картинка",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "descripstion": forms.Textarea(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


from django import forms
from .models import Movies, People
from django.contrib.auth.forms import UserCreationForm


class MovieForm(forms.ModelForm):
    class meta:
        model = Movies
        fields = ['영화번호', '영화제목', '영화감독', '주연배우', '포스터']

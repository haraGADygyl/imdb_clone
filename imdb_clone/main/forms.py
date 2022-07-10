from django import forms

from imdb_clone.main.models import Movie, Rating


class MovieCreateForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"


class RateForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rate"]

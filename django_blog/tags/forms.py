from django import forms

from .models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name", "slug")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
        }

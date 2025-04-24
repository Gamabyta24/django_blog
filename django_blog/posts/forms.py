from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "slug", "content", "category", "tags")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

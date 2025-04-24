from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First name")
    last_name = forms.CharField(max_length=30, required=True, label="Last name")

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user_instance = getattr(self, "instance", None)

        if (
            user_instance
            and User.objects.filter(username=username)
            .exclude(pk=user_instance.pk)
            .exists()
        ):
            raise forms.ValidationError("A user with that username already exists.")
        elif not user_instance and User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")

        return username

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserRegistrationForm

# Create your views here.


class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "Пользователь успешно создан")
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
    next_page = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, "Вы вошли")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы вышли")
        return super().dispatch(request, *args, **kwargs)

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.

def index(request):
    return render(request,'users/index.html')

class UserCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "User successfully registered")
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "users/login.html"
    next_page = reverse_lazy("index")

    def form_valid(self, form):
        messages.success(self.request, "You are logged in")
        return super().form_valid(form)
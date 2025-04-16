from django.urls import path

from .views import index

from .views import UserCreateView,UserLoginView,UserLogoutView

urlpatterns = [
    path("", index, name="index"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
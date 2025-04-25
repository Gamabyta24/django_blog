"""
URL configuration for django_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from .views import PostListView, UniversalDeleteView , HomePageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    path("page/<int:page>/", PostListView.as_view(), name="posts_paginated"),
    path("users/", include("django_blog.users.urls")),
    path("tags/", include("django_blog.tags.urls")),
    path("posts/", include("django_blog.posts.urls")),
    path("categories/", include("django_blog.categories.urls")),
    path(
        "delete/<str:model_name>/<int:pk>/",
        UniversalDeleteView.as_view(),
        name="universal_delete",
    ),
]

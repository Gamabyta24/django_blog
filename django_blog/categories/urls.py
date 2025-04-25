from django.urls import include, path

import django_blog.categories.views as views
from django_blog.views import UniversalDeleteView

urlpatterns = [
    path("", views.CategoryListView.as_view(), name="category_list"),
    path("new/", views.CategoryCreateView.as_view(), name="category_create"),
    path("<slug:slug>/edit/", views.CategoryUpdateView.as_view(), name="category_edit"),
    path("<slug:slug>/delete/", UniversalDeleteView.as_view(), {"model_name": "category"}, name="category_delete"),
    path("category/<slug:slug>/", views.CategoryPostListView.as_view(), name="category_posts"),
]

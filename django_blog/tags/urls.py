from django.urls import include, path

from django_blog.views import UniversalDeleteView

from .views import TagCreateView, TagListView, TagPostListView, TagUpdateView

urlpatterns = [
    path("", TagListView.as_view(), name="tag_list"),
    path("new/", TagCreateView.as_view(), name="tag_create"),
    path("<slug:slug>/", TagPostListView.as_view(), name="tag_posts"),
    path("<slug:slug>/edit/", TagUpdateView.as_view(), name="tag_edit"),
    path(
        "<slug:slug>/delete/",
        UniversalDeleteView.as_view(),
        {"model_name": "tag"},
        name="tag_delete",
    ),
]

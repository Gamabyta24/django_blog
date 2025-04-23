from django.urls import path,include
from .views import TagListView, TagPostListView, TagCreateView, TagUpdateView
from django_blog.views import UniversalDeleteView
urlpatterns = [
    path('', TagListView.as_view(), name='tag_list'),
    path('new/', TagCreateView.as_view(), name='tag_create'),
    path('<slug:slug>/', TagPostListView.as_view(), name='tag_posts'),
    path('tag/<slug:slug>/edit/', TagUpdateView.as_view(), name='tag_edit'),
    path('<slug:slug>/delete/', UniversalDeleteView.as_view(), {'model_name': 'tag'},name='tag_delete'),
    ]
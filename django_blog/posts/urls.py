from django.urls import path,include
from .views import PostCreateView , PostUpdateView ,  PostListView , PostDetailView
from django_blog.views import UniversalDeleteView
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('new/', PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<slug:slug>/delete/', UniversalDeleteView.as_view(),{'model_name': 'post'}, name='post_delete'),
    ]
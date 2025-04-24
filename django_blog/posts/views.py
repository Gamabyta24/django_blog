from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView , ListView
from .models import Post
from django_blog.categories.models import Category
from django_blog.tags.models import Tag
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'posts/index.html')


class PostListView(ListView):  # Было: PostDetailView(DetailView)
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-created_date')

        # Фильтрация по категориям
        categories = self.request.GET.getlist('categories')
        if categories:
            queryset = queryset.filter(category__id__in=categories)

        # Фильтрация по тегам
        tags = self.request.GET.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__id__in=tags).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['selected_categories'] = self.request.GET.getlist('categories')
        context['selected_tags'] = self.request.GET.getlist('tags')
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        # Эти переменные нужны для отображения checked-состояний
        context['selected_categories'] = self.request.GET.getlist('categories')
        context['selected_tags'] = self.request.GET.getlist('tags')

        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Пост успешно создан!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание поста'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Пост успешно обновлен!')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование поста'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'delete_confirmation.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Пост успешно удален!')
        return super().delete(request, *args, **kwargs)
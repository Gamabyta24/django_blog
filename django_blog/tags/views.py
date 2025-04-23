from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
from django_blog.posts.models import Post
from django_blog.tags.models import Tag
from django_blog.categories.models import Category
from .forms import TagForm
# Create your views here.
def index(request):
    return render(request, 'tags/index.html')

class TagListView(ListView):
    model = Tag
    template_name = 'tags/tag_list.html'
    context_object_name = 'tags'

class TagPostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return tag.posts.all().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['current_tag'] = tag
        context['title'] = f'Посты с тегом: {tag.name}'
        return context


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        messages.success(self.request, 'Тег успешно создан!')
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = 'tags/tag_form.html'
    success_url = reverse_lazy('tag_list')

    def form_valid(self, form):
        messages.success(self.request, 'Тег успешно обновлен!')
        return super().form_valid(form)
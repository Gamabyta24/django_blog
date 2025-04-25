from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from django_blog.tags.models import Tag

from .forms import TagForm

# Create your views here.


class TagListView(ListView):
    model = Tag
    template_name = "tags/tag_list.html"
    context_object_name = "tags"


class TagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/tag_form.html"
    success_url = reverse_lazy("tag_list")

    def form_valid(self, form):
        messages.success(self.request, "Тег успешно создан!")
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/tag_form.html"
    success_url = reverse_lazy("tag_list")

    def form_valid(self, form):
        messages.success(self.request, "Тег успешно обновлен!")
        return super().form_valid(form)

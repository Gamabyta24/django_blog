from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import CategoryForm
from .models import Category


class CategoryListView(ListView):
    model = Category
    template_name = "categories/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        messages.success(self.request, "Категория успешно создана!")
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("category_list")

    def form_valid(self, form):
        messages.success(self.request, "Категория успешно обновлена!")
        return super().form_valid(form)

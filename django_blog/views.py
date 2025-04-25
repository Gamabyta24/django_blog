from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import DeleteView

from django_blog.categories.models import Category
from django_blog.posts.models import Post
from django_blog.tags.models import Tag


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        return context


class UniversalDeleteView(DeleteView):
    template_name = "delete_confirmation.html"

    def get_object(self, queryset=None):
        model_name = self.kwargs.get("model_name")
        slug = self.kwargs.get("slug")

        models = {
            "post": Post,
            "category": Category,
            "tag": Tag,
        }

        model = models.get(model_name)
        if not model:
            raise ValueError(f"Модель '{model_name}' не поддерживается.")

        return get_object_or_404(model, slug=slug)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.kwargs.get("model_name") == "post":
            if obj.author != request.user:
                messages.error(
                    request,
                    "Вы не являетесь автором этого поста и не можете его удалить.",
                )
                raise PermissionDenied("Недостаточно прав для удаления.")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        object_name = str(obj)
        model_name = self.kwargs.get("model_name")
        messages.success(
            request, f"{model_name.title()} «{object_name}» успешно удалён."
        )
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        model_name = self.kwargs.get("model_name")
        success_urls = {
            "post": reverse_lazy("home"),
            "category": reverse_lazy("category_list"),
            "tag": reverse_lazy("tag_list"),
        }
        return success_urls.get(model_name, reverse_lazy("home"))


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добро пожаловать в Django Blog"
        return context

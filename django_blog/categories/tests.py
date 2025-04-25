from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Category


class CategoryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="pass1234"
        )
        self.category = Category.objects.create(
            name="Sample Category", slug="sample-category"
        )

    def test_category_list_view(self):
        response = self.client.get(reverse("category_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "categories/category_list.html")
        self.assertContains(response, "Sample Category")
        self.assertIn("categories", response.context)

    def test_category_create_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("category_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_category_create_view_success(self):
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(
            reverse("category_create"),
            {"name": "New Category", "slug": "new-category"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name="New Category").exists())

    def test_category_update_view_success(self):
        self.client.login(username="testuser", password="pass1234")
        url = reverse(
            "category_edit", kwargs={"slug": self.category.slug}
        )  # обновлённый маршрут
        response = self.client.post(
            url, {"name": "Updated Category", "slug": "updated-category"}
        )
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Category")

    def test_category_update_requires_login(self):
        url = reverse("category_edit", kwargs={"slug": self.category.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_category_delete_view_success(self):
        self.client.login(username="testuser", password="pass1234")
        url = reverse(
            "category_delete",
            kwargs={"model_name": "category", "slug": self.category.slug},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        # Объект должен быть удалён
        self.assertFalse(
            Category.objects.filter(slug=self.category.slug).exists()
        )

    def test_category_delete_requires_login(self):
        url = reverse(
            "category_delete",
            kwargs={"model_name": "category", "slug": self.category.slug},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

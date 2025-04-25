from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from django_blog.tags.models import Tag


class TagViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="pass1234"
        )
        self.tag = Tag.objects.create(name="Python", slug="python")

    def test_tag_list_view(self):
        response = self.client.get(reverse("tag_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tags/tag_list.html")
        self.assertContains(response, "Python")
        self.assertIn("tags", response.context)

    def test_tag_create_view_requires_login(self):
        response = self.client.get(reverse("tag_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_tag_create_view_success(self):
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(
            reverse("tag_create"), {"name": "Django", "slug": "django"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tag.objects.filter(name="Django").exists())

    def test_tag_update_view_requires_login(self):
        url = reverse("tag_edit", kwargs={"slug": self.tag.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_tag_update_view_success(self):
        self.client.login(username="testuser", password="pass1234")
        url = reverse("tag_edit", kwargs={"slug": self.tag.slug})
        response = self.client.post(
            url, {"name": "Updated Tag", "slug": "updated-tag"}
        )
        self.assertEqual(response.status_code, 302)
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, "Updated Tag")

    def test_tag_delete_view_requires_login(self):
        url = reverse(
            "tag_delete", kwargs={"model_name": "tag", "slug": self.tag.slug}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_tag_delete_view_success(self):
        self.client.login(username="testuser", password="pass1234")
        url = reverse(
            "tag_delete", kwargs={"model_name": "tag", "slug": self.tag.slug}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Tag.objects.filter(slug="python").exists())

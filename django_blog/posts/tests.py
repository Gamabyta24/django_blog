from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from django_blog.posts.models import Category, Post, Tag


class PostViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="pass1234"
        )
        self.category = Category.objects.create(name="Django", slug="django")
        self.tag = Tag.objects.create(name="Python", slug="python")
        self.post = Post.objects.create(
            title="Test Post",
            slug="test-post",
            content="This is a test post",
            author=self.user,
            category=self.category,
        )
        self.post.tags.add(self.tag)

    def test_post_list_view(self):
        response = self.client.get(reverse("post_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_list.html")
        self.assertContains(response, "Test Post")
        self.assertIn("posts", response.context)

    def test_post_create_view_requires_login(self):
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_post_create_view_success(self):
        self.client.login(username="testuser", password="pass1234")
        response = self.client.post(
            reverse("post_create"),
            {
                "title": "New Post",
                "slug": "new-post",
                "content": "This is a new post",
                "category": self.category.id,
                "tags": [self.tag.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="New Post").exists())

    def test_post_update_view_requires_login(self):
        url = reverse("post_edit", kwargs={"slug": self.post.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)

    def test_post_update_view_success(self):
        self.client.login(username="testuser", password="pass1234")
        url = reverse("post_edit", kwargs={"slug": self.post.slug})
        response = self.client.post(
            url,
            {
                "title": "Updated Post",
                "slug": "updated-post",
                "content": "This is an updated post",
                "category": self.category.id,
                "tags": [self.tag.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Post")

    def test_post_delete_view_success(self):
        self.client.login(username="testuser", password="pass1234")
        url = reverse(
            "post_delete", kwargs={"model_name": "post", "slug": self.post.slug}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(slug="test-post").exists())

    def test_post_detail_view(self):
        response = self.client.get(
            reverse("post_detail", kwargs={"slug": self.post.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "posts/post_detail.html")
        self.assertContains(response, "Test Post")
        self.assertIn("post", response.context)
        self.assertIn("categories", response.context)
        self.assertIn("tags", response.context)

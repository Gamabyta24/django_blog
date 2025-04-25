from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse


class UsersViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.home_url = reverse("home")

    def test_user_registration_success(self):

        response = self.client.post(
            self.register_url,
            {
                "username": "newuser",
                "first_name": "John",
                "last_name": "Doe",
                "password1": "new_user_password",
                "password2": "new_user_password",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        self.assertTrue(User.objects.filter(username="newuser").exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Пользователь успешно создан")

    def test_user_registration_invalid_data(self):

        response = self.client.post(
            self.register_url,
            {
                "username": "newuser",
                "first_name": "John",
                "last_name": "Doe",
                "password1": "short",
                "password2": "short",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_user_login_success(self):

        User.objects.create_user(username="testuser", password="12345")

        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "12345"}
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

        self.assertTrue(response.wsgi_request.user.is_authenticated)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы вошли")

    def test_user_login_invalid_credentials(self):

        response = self.client.post(
            self.login_url,
            {"username": "nonexistentuser", "password": "wrongpassword"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_logout(self):

        User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

        response = self.client.post(self.logout_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Вы вышли")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

        response = self.client.get(reverse("home"))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

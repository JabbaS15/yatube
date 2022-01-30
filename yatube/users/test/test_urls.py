from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class UserURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username='TestURLUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_response_for_all_users(self):
        """Страница из списка доступна любому пользователю."""
        correct_response = [
            '/auth/login/',
            '/auth/logout/',
            '/auth/signup/',
            '/auth/password_reset/',
            '/auth/password_reset/done/',
            '/auth/reset/MTE/set-password/',
            '/auth/reset/done/',
        ]

        for url in correct_response:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_response_for_authorized_users(self):
        """Страница из списка доступна авторизованному пользователю."""
        correct_response = [
            '/auth/password_change/',
            '/auth/password_change/done/',
        ]

        for url in correct_response:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_users_urls_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/auth/password_change/': 'users/password_change_form.html',
            '/auth/password_change/done/': 'users/password_change_done.html',
            '/auth/logout/': 'users/logged_out.html',
            '/auth/login/': 'users/login.html',
            '/auth/signup/': 'users/signup.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
            '/auth/password_reset/done/': 'users/password_reset_done.html',
            '/auth/reset/MTE/set-password/':
                'users/password_reset_confirm.html',
            '/auth/reset/done/': 'users/password_reset_complete.html',
        }

        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

from http import HTTPStatus

from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_urls_uses_correct_response(self):
        """Страница из списка доступна любому пользователю."""
        correct_response = [
            '/about/author/',
            '/about/tech/',
        ]

        for url in correct_response:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }

        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

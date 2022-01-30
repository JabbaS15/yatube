from http import HTTPStatus

from .test_views import PostCreateModule


class PostURLTests(PostCreateModule):

    def test_urls_uses_correct_response_for_authorized_users(self):
        """Страница из списка доступна авторизованному пользователю."""
        correct_response = [
            '/create/',
            f'/posts/{self.post.pk}/edit/',
        ]

        for url in correct_response:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_redirect_anonymous_on_admin_login(self):
        """Страница из списка перенаправит анонимного пользователя
        на страницу логина.
        """
        templates_url_redirect = {
            '/create/': '/auth/login/?next=/create/',
            f'/posts/{self.post.pk}/edit/':
                f'/auth/login/?next=/posts/{self.post.pk}/edit/',
        }

        for url, template in templates_url_redirect.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertRedirects(response, template)

    def test_urls_uses_correct_response_for_all_users(self):
        """Страница из списка доступна любому пользователю."""
        correct_response = [
            '/',
            f'/profile/{self.user}/',
            f'/posts/{self.post.pk}/',
            f'/group/{self.group.slug}/',
        ]

        for url in correct_response:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_urls_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/profile/{self.user}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
        }

        for url, template in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

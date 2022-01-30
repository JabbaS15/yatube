from django import forms

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()


class UserURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create(username='TestURLUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:password_change'
                    ): 'users/password_change_form.html',
            reverse('users:password_change_done'
                    ): 'users/password_change_done.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:logout'): 'users/logged_out.html',
            reverse('users:password_reset_form'
                    ): 'users/password_reset_form.html',
            reverse('users:password_reset_done'
                    ): 'users/password_reset_done.html',
            reverse(
                'users:password_reset_complete'
            ): 'users/password_reset_complete.html',
            reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': 'MTE',
                        'token': 'set-password'}
            ): 'users/password_reset_confirm.html',
        }

        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_show_correct_context(self):
        """Форма /signup сформирована с правильным контекстом."""
        response = self.authorized_client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

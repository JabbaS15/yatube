from ..forms import CreationForm, User
from django.test import Client, TestCase
from django.urls import reverse


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestFormsUser')
        cls.form = CreationForm()

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='TestFormsUser')

    def test_create_form_user(self):
        user_count = User.objects.count()
        form_data = {
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'username': 'TestFromDataUser',
            'email': 'TestUser@yandex.kz',
            'password1': 'QwertY12345678QwertY',
            'password2': 'QwertY12345678QwertY',
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(User.objects.count(), user_count + 1)
        self.assertTrue(
            User.objects.filter(
                first_name='TestFirstName',
                last_name='TestLastName',
                username='TestFromDataUser',
                email='TestUser@yandex.kz',
            ).exists()
        )

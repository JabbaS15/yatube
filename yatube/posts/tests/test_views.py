import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms

from ..forms import PostForm
from ..models import Post, Group, User, Comment, Follow
from ..views import TLIMIT

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateModule(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(username='TestUser')
        cls.user_2 = User.objects.create_user(username='TestUser_2')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.form = PostForm()
        cls.create_text = 'Create_post_form_data'
        cls.edit_text = 'Edit_post_form_data'
        cls.group = Group.objects.create(
            title='Тест group title',
            slug='slug',
            description='Тест group description',
        )
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )

        cls.uploaded_image = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст поста больше 15 символов для контроля проверки',
            group=cls.group,
            image=cls.uploaded_image,

        )

    def setUp(self):
        cache.clear()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_status_project(self):
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(response.status_code, 200)


class PostsPagesTest(PostCreateModule):

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}
                    ): 'posts/group_list.html',
            reverse('posts:profile',
                    kwargs={'username': self.user}): 'posts/profile.html',
            reverse('posts:post_detail',
                    kwargs={
                        'post_id': self.post.pk}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit',
                    kwargs={
                        'post_id': self.post.pk}): 'posts/create_post.html',
        }
        for url, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_page_obj_show_correct_context(self):
        """Шаблоны из списка сформированы с правильным контекстом."""
        templates_page = [
            reverse('posts:index'),
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': self.user}),
        ]
        for url in templates_page:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                context_objects = response.context['page_obj'][0]
                self.assertEqual(context_objects.text, self.post.text)
                self.assertEqual(context_objects.author.username,
                                 self.post.author.username)
                self.assertEqual(context_objects.group, self.post.group)
                self.assertEqual(context_objects.image, self.post.image)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}))
        context_objects = response.context['post']
        self.assertEqual(context_objects.text, self.post.text)
        self.assertEqual(context_objects.author.username,
                         self.post.author.username)
        self.assertEqual(context_objects.group, self.post.group)
        self.assertEqual(context_objects.image, self.post.image)

    def test_show_correct_context(self):
        """Форма из списка сформированы с правильным контекстом."""
        templates_page = [
            reverse('posts:post_create'),
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
        ]
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for url in templates_page:
            response = self.authorized_client.get(url)
            for value, form_value in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context.get('form'
                                                      ).fields.get(value)
                    self.assertIsInstance(form_field, form_value)

    def test_new_post_group(self):
        """"Провекрка распределения постов по страницам"""
        templates_page = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user}),
        ]
        for value in templates_page:
            with self.subTest(value=value):
                response = self.client.get(value)
                context_objects = response.context['page_obj'][0]
                self.assertEqual(context_objects.group.pk, self.post.group.pk)
                self.assertIn(self.post.text, context_objects.text)

    def test_post_is_not_another_group(self):
        """"Провекрка постов на наличие в другой группе"""
        new_group = Group.objects.create(
            slug='slug_new_group',
        )
        new_post = Post.objects.create(
            author=self.user,
            group=new_group,
        )
        response = self.client.get(reverse(
            'posts:group_list', kwargs={'slug': self.group.slug}))
        context_objects = response.context['page_obj']
        self.assertNotIn(new_post, context_objects)

    def test_commentary_for_add_comment(self):
        """"Проверка отправки комментария на страницу поста"""
        comment_post = Comment.objects.create(
            post=self.post,
            author=self.user,
            text='test_comment_text'
        )
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk}))
        context_objects = response.context['comments'][0]
        self.assertEqual(context_objects.text, comment_post.text)

    def test_add_comment(self):
        """"Проверка добавления коменнтария пользователем"""
        comment_count = Comment.objects.count()
        form_data = {
            'post': self.post,
            'author': self.user,
            'text': 'test_comment_text'
        }
        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}))
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text='test_comment_text',
            ).exists()
        )

    def test_follow(self):
        """"Проверка подписки на автора"""
        user_follow = Follow.objects.count()
        from_data = {
            'user': self.user,
            'author': self.user_2,
        }
        response = self.authorized_client.post(
            reverse('posts:profile_follow', kwargs={'username': self.user_2}),
            data=from_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:follow_index'))
        self.assertEqual(Follow.objects.count(), user_follow + 1)
        self.assertTrue(
            Follow.objects.filter(
                user=self.user,
                author=self.user_2,
            ).exists()
        )

    def test_unfollow(self):
        """"Проверка отписки от автора"""
        Follow.objects.create(
            user=self.user,
            author=self.user_2,
        )
        from_data = {
            'user': self.user,
            'author': self.user_2,
        }
        response = self.authorized_client.post(
            reverse(
                'posts:profile_unfollow', kwargs={'username': self.user_2}),
            data=from_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:follow_index'))
        self.assertEqual(Follow.objects.count(), 0)
        self.assertFalse(
            Follow.objects.filter(
                user=self.user,
                author=self.user_2,
            ).exists()
        )

    def test_follow_context(self):
        """"Проверка отправки поста автора на страницу поста подписчика"""
        Follow.objects.create(
            user=self.user,
            author=self.user_2,
        )
        post_user_2 = Post.objects.create(
            author=self.user_2,
            text='test follow',
            group=self.group,
        )

        response = self.authorized_client.get(reverse('posts:follow_index'))
        context_objects = response.context['page_obj']
        self.assertIn(post_user_2, context_objects)
        self.assertNotIn(self.post, context_objects)


class PaginatorViewsTest(PostCreateModule):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.number_post = 17
        Post.objects.bulk_create([
            Post(
                text='Тестовый текст для 17ти постов',
                author=cls.user,
                group=cls.group,
            ) for i in range(cls.number_post - 1)
        ])

    def test_firs_and_second_page_contains_ten_records(self):
        """"Проверка работы Паджинатора на первой и второй странице"""
        templates_page = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user}),
        ]
        for url in templates_page:
            with self.subTest(url=url):
                response_one_page = self.client.get(url)
                response_two_page = self.client.get(url + '?page=2')
                self.assertEqual(len(response_one_page.context['page_obj']),
                                 TLIMIT)
                self.assertEqual(len(response_two_page.context['page_obj']),
                                 self.number_post - TLIMIT)

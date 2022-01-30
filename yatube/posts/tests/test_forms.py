from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile

from .test_views import PostCreateModule
from ..models import Post
from django.urls import reverse


class PostFormTests(PostCreateModule):

    def test_create_form_post(self):
        """Проверка формы create_form для создания поста"""
        post_count = Post.objects.count()
        uploaded = SimpleUploadedFile(
            name='small_2.gif',
            content=self.small_gif,
            content_type='image/gif'
        )
        form_data = {
            'author': self.user,
            'text': self.create_text,
            'group': self.group.pk,
            'image': uploaded
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user}))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text=self.create_text,
                group=self.group.pk,
                image='posts/small_2.gif'
            ).exists()
        )

    def test_edit_form_post(self):
        """Проверка формы edit_form для редактирования поста"""
        post_count = Post.objects.count()
        form_data = {
            'author': self.user,
            'text': self.edit_text,
            'group': self.group.pk,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}))
        self.assertEqual(Post.objects.count(), post_count)
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text=self.edit_text,
                group=self.group.pk
            ).exists()
        )
        self.assertFalse(
            Post.objects.filter(
                author=self.user,
                text=self.post.text,
                group=self.group.pk
            ).exists()
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

from .test_views import PostCreateModule


class PostModelTest(PostCreateModule):

    def test_models_post_have_correct_object_names(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        self.assertEqual(self.post.text[:15], str(self.post))

    def test_models_group_have_correct_object_names(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        self.assertEqual(self.group.title, str(self.group.title))

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост.',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).help_text, expected)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    self.post._meta.get_field(value).verbose_name, expected)

# Yatube - Социальная сеть для блогеров.
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=013220)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=013220)](https://www.djangoproject.com/)

## Описание проекта:
Сервис для блогеров, позволяет пользователям публикацию постов с изображениями, распределение постов по группам, имеются личные страницы пользователей со стеной, подписка на авторов и комментирование записей. Работает Кэш, имеется покрытие тестами и настроена админ панель.

## Инструкция по развёртыванию:
1. Загрузите проект:
```
git clone https://github.com/JabbaS15/yatube.git
```
2. Установите и активируйте виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```
3. Установите зависимости:
```
pip install -r requirements.txt
```
4. В папке с файлом manage.py выполните команду запуска:
```
python3 manage.py runserver
```

### Unitest тестирование для проекта Yatube
#### Тестирование Models
- для класса Post — первые пятнадцать символов поста: **post.text[:15];
- для класса Group — название группы.
- verbose_name в полях совпадает с ожидаемым
- help_text в полях совпадает с ожидаемым
#### Тестирование URLs
- доступность страниц с авторизацией и без
- соответствие страниц и шаблонов
- проверка 404 страницы
- доступность страницы редактирования поста /posts/post_id/edit/ для
  анонимного пользователя, авторизованных автора и не автора поста;
- проверка используемых редиректов на всех страницах
#### Тестирование Views
- проверка отображения нового поста в фиде подписок
- новый пост появляется на главной странице
- страницы используют правильные шаблоны
- шаблоны сфомированы с правильным контекстом
- тест кэша
- авторизированный юзер может писать комменты (не авторизированный не может)
- создание новой подписки и нельзя подписаться на себя
#### Тест приложения About:
- страницы /about/author/ и /about/tech/ доступны неавторизованному пользователю;
- для отображения страниц /about/author/ и /about/tech/применяются ожидаемые view-функции и шаблоны.
#### Тестирование Forms
- валидная форма создает/изменяет пост

### Автор проекта:
[Шведков Роман](https://github.com/JabbaS15)

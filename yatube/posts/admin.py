from django.contrib import admin
from .models import Post, Group, Comment


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentaryAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'author',
        'text',
        'created',
    )


admin.site.register(Comment, CommentaryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)

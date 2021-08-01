from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Comment, Follow, Group, Post

EMPTY_VALUE_DISPLAY = '-пусто-'

User = get_user_model()


class PostsInstanceInline(admin.TabularInline):
    model = Post


class CommentsInstanceInline(admin.TabularInline):
    model = Comment


class FollowsInstanceInline(admin.TabularInline):
    model = Follow


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'pub_date', 'author', 'group', 'image')
    search_fields = ('text', 'author', 'group', 'image')
    list_filter = ('pub_date', 'author', 'group', 'image')
    inlines = [CommentsInstanceInline]
    empty_value_display = EMPTY_VALUE_DISPLAY


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'description')
    search_fields = ('title', 'description', 'slug')
    list_filter = ('title',)
    inlines = [PostsInstanceInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created', 'author', 'post')
    search_fields = ('text', 'author', 'post')
    list_filter = ('created', 'author')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'following')
    search_fields = ('user', 'following')
    list_filter = ('user', 'following')


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
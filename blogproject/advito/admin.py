from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django.utils.html import format_html
import datetime
from .models import (Profile, Post, CategoryPost, 
    FavoritePost, Comment, Review, Message
)

# admin.site.register(Post)
admin.site.register(CategoryPost)
# admin.site.register(FavoritePost)
# admin.site.register(Comment)
admin.site.register(Review)
# admin.site.register(Message)


class FavoritePostAdminInline(admin.TabularInline):
    model = FavoritePost
    fieldsets = [
        ('Posts', {'fields': ['post']}),
    ]
    readonly_fields = ['post']
    extra=0

    # def has_add_permission(request):
    #     return False


class MessageAdmininline(admin.StackedInline):
    model = Message
    fields = ['to_whom','in_post','text','date_pub', 'date_edit',]
    extra=0


class ReviewAdmininline(admin.StackedInline):
    model = Review
    fields = ['to_whom','rating','text','date_pub', 'date_edit',]
    extra=0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = [FavoritePostAdminInline, MessageAdmininline, ReviewAdmininline]

    fieldsets = [
        (None, {'fields': ['user']}),
        ('Info', {'fields': ['avatar','birth_date','phone','town','about']}),
        ('Other', {'fields': ['subscribers']}),
    ]
    readonly_fields = ['user']
    list_display = ('user', 'town',)
    list_filter = ( 'town', )
    search_fields = ('town', )


def delete_very_old_post(modeladmin, request, queryset):
    print(dir(queryset))
    queryset.filter(date_pub_lte=timezone.now() - datetime.timedelta(weeks=48)).delete()


class CommentAdmininline(admin.TabularInline):
    model = Comment
    fields = ['author', 'text', 'date_publish']
    extra=0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentAdmininline]
    list_display = ('author', 'date_pub', 'category')
    search_fields = ('date_pub', 'category',)
    list_filter = ('category', 'date_pub', 'author', )

    actions = [delete_very_old_post]

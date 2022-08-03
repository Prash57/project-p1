from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Tag, Image


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'headline', 'user', 'created')
    
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'name', 'body')

admin.site.register(Comment, CommentAdmin)

admin.site.register(Tag)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo')

admin.site.register(Image, ImageAdmin)


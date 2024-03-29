from django.contrib import admin
from .models import BlogType
from .models import Blog

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog_type', 'author', 'created_time', 'last_updated_time', 'get_read_num')
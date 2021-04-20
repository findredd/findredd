from django.contrib import admin
from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'header', 'posted_date', 'tags', 'featured_status')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)

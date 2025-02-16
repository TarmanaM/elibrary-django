from django.contrib import admin
from .models import Book, BookPage

admin.site.register(BookPage)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'published_year', 'is_favorite')
    list_filter = ('genre', 'published_year', 'is_favorite')
    search_fields = ('title', 'author')


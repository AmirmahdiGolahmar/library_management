from django.contrib import admin

from library.models import Book, Author


# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'get_authors', 'publisher', 'picture')
    list_filter = ('genre',)
    search_fields = ('title','author__first_name', 'author__last_name' ,'publisher')
    ordering = ('publish_date',)
    list_per_page = 20

    def get_authors(self, obj):
        return ", ".join([f"{a.first_name} {a.last_name}" for a in obj.author.all()])
    get_authors.short_description = 'authors'

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ( 'last_name', 'first_name', 'id', 'email', 'bio')
    search_fields = ('last_name', 'first_name', 'email')
    list_per_page = 20
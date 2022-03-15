from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models without admin enabled
admin.site.register(Genre)
admin.site.register(Language)

# Register models with admin enabled
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    # Sectioning the fields in detail view
    fieldsets = (
        ('Basic Info', {
            "fields": (
                'book',
                'imprint',
                'id'
            ),
        }),
        ('Availability', {
            "fields": (
                'status',
                'due_back',
                'borrower'
            )
        })
    )

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields to be displayed on records screens
    list_display = ('title', 'author', 'language', 'display_genre')
    # Records filter criterias
    list_filter = ('author', 'genre')
    # Display inline book instances of this books
    inlines = [BooksInstanceInline]

class BooksInline(admin.TabularInline):
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # Displaying order and grouping on detail screens
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    # Display books of this author as inline tabular
    inlines = [BooksInline]
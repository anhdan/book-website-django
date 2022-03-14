from pyexpat import model
from re import template
from statistics import mode
from unicodedata import name
from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre


# Function to show index page:
def index(request):
    """View function for homepage site."""

    # Records counting
    num_books = Book.objects.all().count()
    num_books_great = \
        Book.objects.filter( title__icontains="great" ).count()

    num_authors = Author.objects.count()
    num_genre = Genre.objects.count()


    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # Data to bypass in index.html file
    context = {
        'num_books': num_books,
        'num_books_great': num_books_great,
        'num_genre': num_genre,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


# Class to show books list
class BookListView(generic.ListView):
    model = Book
    paginate_by = 3
    # context_object_name = 'my_book_list' #custom object variable name in template file
    # queryset = Book.objects.all()[:5]
    #template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location


# Class to show book detail
class BookDetailView(generic.DetailView):
    model = Book

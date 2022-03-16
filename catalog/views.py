from pyexpat import model
from re import template
from statistics import mode
from unicodedata import name
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

    # Visit times of a user
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Data to bypass in index.html file
    context = {
        'num_books': num_books,
        'num_books_great': num_books_great,
        'num_genre': num_genre,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
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


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowBookListView( PermissionRequiredMixin, generic.ListView ):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_librarian.html'
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


# homework - showing authors list and author details
class AuthorListView( generic.ListView ):
    model = Author


class AuthorDetailView( generic.DetailView ):
    model = Author
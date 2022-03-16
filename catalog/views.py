from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book, Author, BookInstance, Genre

import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


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



# View function for book renewal form
@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed-books') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


#==== Django generic editing form for author
class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'catalog.can_manage_author'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'catalog.can_manage_author'
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'catalog.can_manage_author'
    model = Author
    success_url = reverse_lazy('authors')


#==== Django generic editing form for book
class BookCreate( PermissionRequiredMixin, CreateView ):
    permission_required = 'catalog.can_manage_book'
    model = Book
    fields = '__all__'

class BookUpdate( UpdateView ):
    permission_required = 'catalog.can_manage_book'
    model = Book
    fields = '__all__'

class BookDelete( DeleteView ):
    permission_required = 'catalog.can_manage_book'
    model = Book
    success_url = reverse_lazy('books')
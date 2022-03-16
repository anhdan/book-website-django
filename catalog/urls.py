from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path( 'mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),

    # homework - showing authors list and author details
    path( 'authors/', views.AuthorListView.as_view(), name='authors' ),
    path( 'author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),

    # homework - showing list of all borrowed books to librarian
    path( 'borrowed/', views.BorrowBookListView.as_view(), name='borrowed-books'),
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

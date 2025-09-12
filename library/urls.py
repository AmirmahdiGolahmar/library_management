from django.urls import path
from .views import home_view, BookListView, BookDetailView, AuthorDetailView, AuthorListView
from .views import (
    AuthorCreateView, AuthorUpdateView, AuthorDeleteView,
    BookCreateView, BookUpdateView, BookDeleteView, BookBulkDeleteView
)
urlpatterns = [
    # ---------- Home ----------
    path("", home_view, name="home"),

    # ---------- Author ----------
    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("author/<int:pk>/", AuthorDetailView.as_view(), name="author-detail"),
    path("books/<int:book_id>/authors/<int:pk>", AuthorDetailView.as_view(), name="book-author-detail"),
    path("authors/new/", AuthorCreateView.as_view(), name="author-create"),
    path("authors/<int:pk>/edit/", AuthorUpdateView.as_view(), name="author-update"),
    path("authors/<int:pk>/delete/", AuthorDeleteView.as_view(), name="author-delete"),

    # ---------- Book ----------
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("authors/<int:author_id>/books/<int:pk>/", BookDetailView.as_view(), name="author-book-detail"),
    path("books/new/", BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/edit/", BookUpdateView.as_view(), name="book-update"),
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
    path("books/bulk-delete/", BookBulkDeleteView.as_view(), name="book-bulk-delete"),

]
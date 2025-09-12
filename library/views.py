from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from .models import Book, Author
from django.db.models import Q
from django.utils.http import urlencode
from django.db.models import Count
from django.db.models import Count, Case, When, Value, CharField
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.views import View
from .forms import BookForm, AuthorForm
from decimal import Decimal, InvalidOperation
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# home view
def home_view(request):
    recent_books = Book.objects.select_related().prefetch_related('author').order_by('-publish_date')[:8]

    genre_map = dict(Book.GENRE_CHOICES)

    genre_counts_qs = (
        Book.objects
        .values('genre')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    genre_counts = []
    for g in genre_counts_qs:
        genre_counts.append({
            'genre': g['genre'],
            'count': g['count'],
            'genre_label': genre_map.get(g['genre'], g['genre'])
        })


    # quick site stats
    stats = {
        'books': Book.objects.count(),
        'authors': Author.objects.count(),
    }

    context = {
        'recent_books': recent_books,
        'genre_counts': genre_counts,
        'stats': stats,
    }
    return render(request, 'home.html', context)

# ---------- Author CRUD ----------
class AuthorListView(ListView):
    model = Author
    template_name = "author_list.html"
    context_object_name = "authors"
    paginate_by = 5

    def get_queryset(self):
        qs = (
            Author.objects
            .annotate(book_count=Count("books", distinct=True))
            .order_by("last_name", "first_name")
            .prefetch_related("books")
        )

        q = (self.request.GET.get("q") or "").strip()
        if q:
            terms = q.split()
            for term in terms:
                qs = qs.filter(
                    Q(first_name__icontains=term) |
                    Q(last_name__icontains=term) |
                    Q(email__icontains=term)
                )

        return qs.distinct()

    @staticmethod
    def _qs_without(params, *keys):
        p = params.copy()
        for k in keys:
            p.pop(k, None)
        return urlencode(p, doseq=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        context["current_qs"] = self._qs_without(params, "page")
        context["current_qs_wo_q"] = self._qs_without(params, "page", "q")
        return context
class AuthorDetailView(LoginRequiredMixin, DetailView):
    model = Author
    template_name = "author_detail.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        book_id = self.kwargs.get("book_id")
        if book_id:
            context["via_book"] = Book.objects.filter(pk=book_id).first()

        if self.request.GET.get("via") == "book":
            context["via_book"] = Book.objects.filter(
                pk=self.request.GET.get("book")
            ).first()

        return context
class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = "author_form.html"
class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = "author_form.html"
class AuthorDeleteView(LoginRequiredMixin, DeleteView):
    model = Author
    template_name = "author_confirm_delete.html"
    success_url = reverse_lazy("author-list")

# ---------- Book CRUD ----------
class FilteredBookQuerysetMixin:
    def build_filtered_qs(self, request):
        qs = (Book.objects
              .all()
              .prefetch_related("author")
              .order_by("-publish_date"))

        q = (request.GET.get("q") or "").strip()
        if q:
            terms = q.split()
            query = Q()
            for term in terms:
                query &= (
                    Q(title__icontains=term) |
                    Q(publisher__icontains=term) |
                    Q(author__first_name__icontains=term) |
                    Q(author__last_name__icontains=term)
                )
            qs = qs.filter(query).distinct()

        genres = request.GET.getlist("genre")
        if genres:
            qs = qs.filter(genre__in=genres)

        min_price_raw = (request.GET.get("min_price") or "").strip()
        max_price_raw = (request.GET.get("max_price") or "").strip()

        def parse_decimal(s):
            if not s:
                return None
            try:
                return Decimal(s)
            except (InvalidOperation, ValueError):
                return None

        min_price = parse_decimal(min_price_raw)
        max_price = parse_decimal(max_price_raw)

        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)

        return qs
class BookListView(FilteredBookQuerysetMixin, ListView):
    model = Book
    template_name = "book_list.html"
    context_object_name = "books"
    paginate_by = 15

    def get_queryset(self):
        return self.build_filtered_qs(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genre_choices"] = Book.GENRE_CHOICES
        context["selected_genres"] = self.request.GET.getlist("genre")
        params = self.request.GET.copy()
        params.pop("page", None)
        context["current_qs"] = urlencode(params, doseq=True)
        context["filtered_count"] = self.get_queryset().count()
        return context
class BookDetailView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = "book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        author_id = self.kwargs.get("author_id")
        if author_id:
            context["via_author"] = Author.objects.filter(pk=author_id).first()

        if self.request.GET.get("via") == "author":
            context["via_author"] = Author.objects.filter(
                pk=self.request.GET.get("author")
            ).first()

        return context
class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "book_form.html"
class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = "book_form.html"
class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = "book_confirm_delete.html"
    success_url = reverse_lazy("book-list")
class BookBulkDeleteView(LoginRequiredMixin, FilteredBookQuerysetMixin, View):

    def post(self, request):
        confirm = request.POST.get("confirm") == "on"
        qs = self.build_filtered_qs(request)
        count = qs.count()

        if not confirm:
            messages.error(request, "Please confirm bulk deletion.")
            # keep filters in url
            return redirect(f"{reverse('book-list')}?{request.META.get('QUERY_STRING', '')}")

        deleted_count, _ = qs.delete()
        messages.success(request, f"Deleted {deleted_count} book(s).")
        return redirect(f"{reverse('book-list')}?{request.META.get('QUERY_STRING', '')}")




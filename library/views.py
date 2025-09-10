"""Views for the library application."""

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from library.models import Book


def login_view(request):
    """Authenticate a user and start a session.

    Displays a login form on GET requests and processes the submitted
    credentials on POST.  If the credentials are valid, the user is
    logged in and redirected to the Django admin index page.
    """

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("admin:index")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


# Placeholder usage of Book to avoid unused import warnings.
_unused = Book

from django.urls import path
from accounts.views import register_view
from django.contrib.auth import views as auth_views
from .views import login_view

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    # urls.py
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"),name="logout",)
]
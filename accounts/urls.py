from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import signup, login

app_name = "accounts"
urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

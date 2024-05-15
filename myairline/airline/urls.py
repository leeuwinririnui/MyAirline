from django.urls import path
from . import views, auth

urlpatterns = [
    path("", views.home, name="home"),
    path("flights", views.flights, name="flights"),
    path("profile", views.profile, name="profile"),
    path("login", auth.login_view, name="login"),
    path("signup", auth.signup_view, name="signup"),
    path("logout", auth.logout_view, name="logout"),
    path("bookings", views.bookings, name="bookings")
]
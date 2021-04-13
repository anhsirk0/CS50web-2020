from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("hotel/<int:id>", views.hotel_view, name="hotel"),
    path("cities", views.cities, name="cities"),
    path("search", views.search_hotels, name="search"),
    path("popular", views.popular_hotels, name="popular"),
    path("profile", views.profile, name="profile"),
    path("book", views.book_hotel, name="book"),
    path("success", views.successful, name="success"),
    path("track", views.track_booking, name="track"),
    path("callback", views.callback, name="callback"),
]

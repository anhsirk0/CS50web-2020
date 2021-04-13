from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_list, name="create_list"),
    path("item/<int:id>", views.item_view, name="item"),
    path("item/add_watchlist/<int:id>", views.add_watchlist, name="add_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("notification", views.notification, name="notification"),
    path("category/<str:name>", views.category, name="category"),
]

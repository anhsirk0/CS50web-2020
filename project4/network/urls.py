
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("create_post", views.create_post, name="create_post"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path("test", views.test, name="test"),
    path("update", views.update_profile, name="update"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("following", views.following, name="following"),
]

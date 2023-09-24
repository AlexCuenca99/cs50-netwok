from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create-post", views.create_post, name="create-post"),
    path("edit-post/<int:id>", views.edit_post, name="edit-post"),
    path("profiles/<str:username>", views.profile, name="profiles"),
    path("following", views.following, name="following"),
]

from django.urls import path

from posts import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("add/", views.AddpostView.as_view(), name="add-post"),
    path("post/<int:pk>/like/", views.PostLikeView.as_view(), name="post-like"),
]

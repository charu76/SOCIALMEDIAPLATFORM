from django.urls import path
from . import views

urlpatterns = [
    path("", views.feed_view, name="feed"),
    path("explore/", views.explore_view, name="explore"),
    path("signup/", views.signup_view, name="signup"),

    path("post/<int:pk>/", views.post_detail_view, name="post_detail"),
    path("post/<int:pk>/delete/", views.post_delete_view, name="post_delete"),
    path("post/<int:pk>/like/", views.like_toggle_view, name="like_toggle"),
    path("comment/<int:pk>/delete/", views.comment_delete_view, name="comment_delete"),

    path("u/<str:username>/", views.profile_view, name="profile"),
    path("u/<str:username>/follow/", views.follow_toggle_view, name="follow_toggle"),
    path("u/<str:username>/followers/", views.follower_list_view, name="followers"),
    path("u/<str:username>/following/", views.following_list_view, name="following"),
    path("profile/edit/", views.profile_edit_view, name="profile_edit"),
]

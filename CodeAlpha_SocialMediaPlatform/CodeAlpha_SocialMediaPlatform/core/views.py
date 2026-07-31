from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import SignUpForm, PostForm, CommentForm, ProfileForm
from .models import Post, Comment, Like, Follow, Profile


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account was created.")
            return redirect("feed")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def feed_view(request):
    """Posts from people the user follows + their own posts."""
    following_ids = request.user.following.values_list("following_id", flat=True)
    posts = Post.objects.filter(
        Q(author_id__in=following_ids) | Q(author=request.user)
    ).select_related("author", "author__profile")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post published.")
            return redirect("feed")
    else:
        form = PostForm()

    liked_post_ids = set(
        Like.objects.filter(user=request.user, post__in=posts).values_list("post_id", flat=True)
    )
    return render(request, "core/feed.html", {
        "posts": posts, "form": form, "liked_post_ids": liked_post_ids,
    })


@login_required
def explore_view(request):
    """All posts, useful for discovering new people to follow."""
    posts = Post.objects.exclude(author=request.user).select_related("author", "author__profile")
    liked_post_ids = set(
        Like.objects.filter(user=request.user, post__in=posts).values_list("post_id", flat=True)
    )
    following_ids = set(request.user.following.values_list("following_id", flat=True))
    return render(request, "core/explore.html", {
        "posts": posts, "liked_post_ids": liked_post_ids, "following_ids": following_ids,
    })


@login_required
def post_detail_view(request, pk):
    post = get_object_or_404(Post.objects.select_related("author"), pk=pk)
    comments = post.comments.select_related("author")
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", pk=pk)
    else:
        form = CommentForm()
    liked_post_ids = set()
    if Like.objects.filter(post=post, user=request.user).exists():
        liked_post_ids.add(post.pk)
    return render(request, "core/post_detail.html", {
        "post": post, "comments": comments, "form": form, "liked_post_ids": liked_post_ids,
    })


@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
    return redirect("feed")


@login_required
def like_toggle_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    next_url = request.POST.get("next") or request.GET.get("next") or "feed"
    return redirect(next_url)


@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk, author=request.user)
    post_pk = comment.post_id
    if request.method == "POST":
        comment.delete()
    return redirect("post_detail", pk=post_pk)


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = profile_user.posts.all()
    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
    return render(request, "core/profile.html", {
        "profile_user": profile_user, "posts": posts, "is_following": is_following,
    })


@login_required
def profile_edit_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "core/profile_edit.html", {"form": form})


@login_required
def follow_toggle_view(request, username):
    target = get_object_or_404(User, username=username)
    if target != request.user:
        follow, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if not created:
            follow.delete()
    return redirect("profile", username=username)


@login_required
def follower_list_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    followers = [f.follower for f in profile_user.followers.select_related("follower")]
    return render(request, "core/user_list.html", {
        "title": f"People following {profile_user.username}", "users": followers,
    })


@login_required
def following_list_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    following = [f.following for f in profile_user.following.select_related("following")]
    return render(request, "core/user_list.html", {
        "title": f"People {profile_user.username} follows", "users": following,
    })

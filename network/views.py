from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by("-created")

    posts_per_page = 10
    paginator = Paginator(posts, posts_per_page)
    page_number = request.GET.get("page", posts_per_page)
    page_obj = paginator.get_page(page_number)

    data = {"all_posts": posts, "posts_obj": page_obj}

    return render(request, "network/index.html", data)


# View to display all post of users the logged user is following
def following(request):
    user = request.user
    following_users = user.followers.all()

    posts = Post.objects.filter(author_id__in=following_users.values("following_id"))
    all_posts = {"all_posts": posts}
    return render(request, "network/following.html", all_posts)


def profile(request, username):
    user = get_object_or_404(User, username=username)

    followers_count = user.followings.all().count()
    followings_count = user.followers.all().count()
    user_posts = user.authors.all()

    posts_per_page = 10
    paginator = Paginator(user_posts, posts_per_page)
    page_number = request.GET.get("page", posts_per_page)
    page_obj = paginator.get_page(page_number)

    user_posts = page_obj

    user_data = {
        "user_data": user,
        "followers": followers_count,
        "followings": followings_count,
        "posts": user_posts,
    }
    return render(request, "network/profile.html", user_data)


def create_post(request):
    if request.method == "POST":
        # Get auth user
        user = request.user
        content = request.POST["content"]

        # Create POST instance
        try:
            Post.objects.create(content=content, author=user)
        except Exception as e:
            raise Exception("Something went wrong", e)

        return HttpResponseRedirect(reverse(index))


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

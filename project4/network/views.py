from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import *

def test(request):
    return render(request, "network/test.html")

def index(request):
    posts = Post.objects.all().order_by("-id")
    p = Paginator(posts,5)
    try:
        page_num = request.GET["page"]
    except:
        page_num = 1
    page_obj = p.get_page(page_num)
    try:
        liked_posts = [like.post.id for like in request.user.like.all()]
    except:
        liked_posts = []
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "liked_posts": liked_posts
    })

@login_required(login_url='login')
def create_post(request):
    text = request.POST["text"]
    user = request.user
    p = Post(owner=user, text=text)
    p.save()
    return HttpResponseRedirect(reverse("index"))

def profile(request, name):
    try:
        user = User.objects.get(username=name)
        posts = Post.objects.filter(owner=user).order_by("-id")
        p = Paginator(posts,5)
        try:
            page_num = request.GET["page"]
        except:
            page_num = 1
        page_obj = p.get_page(page_num)
        followers = [f.follower for f in user.following.all()]

    except:
        user = None
    
    if request.user.is_authenticated:
        liked_posts = [like.post.id for like in request.user.like.all()]
        is_follower = Follow.objects.filter(follower=request.user, following=user).exists()

    else:
        liked_posts = []
        is_follower = False

    if user:
        return render(request, "network/profile.html", {
            "profile": user,
            "page_obj": page_obj,
            "liked_posts": liked_posts,
            "is_follower": is_follower,
            "followers": followers

        })

    return render(request, "network/apology.html", {
        "message": "User Does not exist"
    })

@login_required(login_url="login")
def following(request):
    user = request.user

    followings = [i.following for i in user.follower.all()]

    following_posts = Post.objects.filter(owner__in=followings).order_by('-id')
    liked_posts = [post.id for post in following_posts if Like.objects.filter(post=post,liked_by=user).exists()]
    
    p = Paginator(following_posts,5)
    try:
        page_num = request.GET["page"]
    except:
        page_num = 1
    page_obj = p.get_page(page_num)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "liked_posts":liked_posts

    })


@login_required(login_url="login")
def update_profile(request):
    if request.method != "POST":
        return render(request, "network/apology.html", {
            "message": "Page Does not exist"
        })
    
    fname = request.POST["fname"]
    lname = request.POST["lname"]
    imgurl = request.POST["imgurl"]
    
    user = request.user

    user.first_name = fname
    user.last_name = lname
    user.imgurl = imgurl
    user.save()

    username = user.username

    return HttpResponseRedirect(reverse("profile", kwargs={'name':username}))


@csrf_exempt
@login_required(login_url="login")
def like(request):
    if request.method != "POST":
        return render(request, "network/apology.html", {
            "message": "Page Does not exist"
        })
    data = json.loads(request.body)
    post_id = int(data.get("id"))
    post = Post.objects.get(id = post_id)
    liked_by = request.user

    like, created = Like.objects.get_or_create(post=post, liked_by=liked_by)

    if not created:
        like.delete()
        print("deleted")
    else:
        like.save()
        print("saved")
    return JsonResponse({"message": "Post liked successfully."}, status=201)
    
@csrf_exempt
@login_required(login_url="login")
def edit_post(request):
    if request.method != "POST":
        return render(request, "network/apology.html", {
            "message": "Page Does not exist"
        })

    data = json.loads(request.body)
    post_id = int(data.get("id"))
    new_text = data.get("text")
    try:
        post = Post.objects.get(id = post_id)
        if post.owner != request.user:
            return render(request, "network/apology.html", {
            "message": "Page Does not exist"
        })

        post.text = new_text
        post.save()
    except:
        pass    
    return JsonResponse({"message": "Post updated successfully."}, status=201)
    
@csrf_exempt
@login_required(login_url="login")
def follow(request):
    if request.method != "POST":
        return render(request, "network/apology.html", {
            "message": "Page Does not exist"
        })
    data = json.loads(request.body)
    username = data.get("username")
    user = User.objects.get(username=username)
    print(user)

    follow , created = Follow.objects.get_or_create(follower=request.user, following=user)
    if not created:
        follow.delete()
        print("deleted")
    else:
        follow.save()
        print("saved")
    
    return JsonResponse({"message": "Followed successfully."}, status=201)

def login_view(request):
    if request.user.is_authenticated:
        return render(request, "network/apology.html", {
            "message": "You are already logged in"
        })

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.user.is_authenticated:
        return render(request, "network/apology.html", {
            "message": "You are already logged in"
        })
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        fname = request.POST["fname"]
        lname = request.POST["lname"]

        print(fname, lname)

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

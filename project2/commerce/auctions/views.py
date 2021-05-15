from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *


@login_required(login_url="login")
def create_list(request):
    categories = [i[0] for i in Auction_item.categories]
    if request.method == "POST":
        name = request.POST["name"].capitalize()
        price = float(request.POST["price"])
        about = request.POST["about"].capitalize()
        imgurl = request.POST["url"]
        category = request.POST["category"]
        owner = request.user
        item = Auction_item(name=name, price=price, owner=owner,
                            imgurl=imgurl, about=about, category=category)
        item.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {"rows": categories})


@login_required(login_url="login")
def item_view(request, id):
    item = Auction_item.objects.get(id=id)
    user = request.user
    in_watchlist = False
    all_items = item.watchlist.all()
    for i in all_items:
        if i.owner == user:
            in_watchlist = True
            break

    if request.method == "POST":
        if "bid_btn" in request.POST:
            bid_value = float(request.POST["bid_value"])
            max_bid = item.max_bid
            # filter + first -> returns None
            if bid_value > max_bid:
                item.max_bid = bid_value
                item.winner = request.user
                item.save()
            q = Bid.objects.filter(bidder=user, item=item).first()
            if not q:
                b = Bid(bidder=user, item=item, bid=bid_value)
                b.save()
            else:
                q.bid = bid_value
                q.save()
            text = f"{user.username} placed a bid of {bid_value}$ on item '{item.name}'"
            Notification(user=item.owner, text=text, item=item,
                         type="bid", color="blue").save()

        if "comment_btn" in request.POST:
            text = request.POST["comment"]
            c = Comment(text=text, commented_by=user, item=item)
            c.save()
            text = f"{user.username} commented on item - '{item.name}'"
            Notification(user=item.owner, text=text,
                         item=item, type="comment").save()

        if "active_btn" in request.POST:
            state = request.POST["state"]
            if state == "unactive":
                item.active = False
                item.save()
                if item.max_bid != 0:
                    text = f"You won the auction on item - '{item.name}'"
                    Notification(user=item.winner, text=text,
                                 item=item, type="win", color="green").save()

    return render(request, "auctions/item.html", {
        "item": item,
        "in_watchlist": in_watchlist,
    })


@login_required(login_url="login")
def add_watchlist(request, id):
    item = Auction_item.objects.get(id=id)
    user = request.user
    w = Watchlist.objects.get(owner=user)
    do = request.GET["do"]
    if do == "add":
        w.item.add(item)
        w.save()
    else:
        w.item.remove(item)
    return redirect(item_view, id=id)


@login_required(login_url="login")
def watchlist(request):
    user = request.user
    w_items = user.watchlist.first().item.all().order_by("-id")
    return render(request, "auctions/watchlist.html", {
        "list": w_items
    })


@login_required(login_url="login")
def notification(request):
    user = request.user
    all = user.notifications.all().order_by("-id")
    n = user.notifications.filter(seen=False)
    for i in n:
        i.seen = True
        i.save()
    return render(request, "auctions/notification.html", {
        "list": all
    })


def category(request, name="all"):
    categories = [
        {
            "name": "All",
            "icon": "view_comfy",
        },
        {
            "name": "Books",
            "icon": "books",
        },
        {
            "name": "Clothing",
            "icon": "style",
        },
        {
            "name": "Electronics",
            "icon": "power",
        },
        {
            "name": "Home",
            "icon": "weekend",
        },
        {
            "name": "Toys",
            "icon": "toys",
        },
        {
            "name": "Other",
            "icon": "widgets",
        },

    ]
    l = Auction_item.objects.filter(active=True).order_by("-id")
    if name != "all":
        l = Auction_item.objects.filter(category=name)
    return render(request, "auctions/category.html", {
        "list": l,
        "categories": categories,
        "name": name
    })


def index(request):
    return render(request, "auctions/index.html", {
        "list": Auction_item.objects.filter(active=True).order_by("-id"),
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            # create empty watchlist
            w = Watchlist(owner=user)
            w.save()

        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

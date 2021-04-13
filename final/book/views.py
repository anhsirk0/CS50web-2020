from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import math
import time

from paytm import Checksum
from .models import *

# Create your views here.
def index(request):
    popular = Hotel.objects.filter(rating = '5 star')
    return render(request, "book/index.html" ,{
        "popular": popular[8:14]
    })

def cities(request):
    cities = Hotel.objects.values('city').distinct()
    new = {city["city"]:None for city in cities}
    return JsonResponse(new, safe=False)


def search_hotels(request):
    try:
        q = request.GET["q"]
        q = q[0].upper()+ q[1:]
        try:
            sort = request.GET["sort"]
        except:
            sort = "def"
        if sort == "r_asc":
            all_hotels = Hotel.objects.filter(city = q).order_by('-rating')
        elif sort == "r_desc":
            all_hotels = Hotel.objects.filter(city = q).order_by('rating')
        elif sort == "p_asc":
            all_hotels = Hotel.objects.filter(city = q).order_by('-price')
        elif sort == "p_desc":
            all_hotels = Hotel.objects.filter(city = q).order_by('price')
        else:
            all_hotels = Hotel.objects.filter(city = q)
            sort = "def"
    except:
        q = None
        all_hotels = None

    if len(request.GET) < 1:
        return render(request, "book/search.html", {
            "message" : "Search Hotels"
        })

    if not all_hotels:
        return render(request, "book/search.html", {
            "message" : "City not found"
        })

    p = Paginator(all_hotels,6)
    try:
        page_num = request.GET["page"]
    except:
        page_num = 1
    page_obj = p.get_page(page_num)
    return render(request, "book/search.html", {
        "page_obj": page_obj,
        "city": q,
        "sort": sort,
        "total": len(all_hotels),
    })

def popular_hotels(request):
    popular = Hotel.objects.filter(rating = '5 star')
    p = Paginator(popular,5)
    try:
        page_num = request.GET["page"]
    except:
        page_num = 1
    page_obj = p.get_page(page_num)
    return render(request, "book/popular.html" ,{
        "page_obj": page_obj
    })

def hotel_view(request, id):
    hotel = Hotel.objects.get(id=id)

    return render(request, "book/hotel.html",{
        "hotel": hotel,
    })

def create_price(id, room, adult, child, days):
    original_price = Hotel.objects.get(id=id).price
    price = original_price * room
    price += math.floor(original_price * (adult - 1) * 0.5)
    price += math.floor(original_price * child / 4)
    price += math.floor(original_price * (days - 1) / 3)
    return price


# @login_required(login_url="login")
def book_hotel(request):
    if request.method != "POST":
        return render(request, "book/book.html", {
            "message": "Page does not exist"
        })

    room = int(request.POST["room"])
    adult = int(request.POST["adult"])
    child = int(request.POST["child"])

    days = int(request.POST["days"])
    id = int(request.POST["id"])

    checkin = request.POST["checkin"]
    checkout = request.POST["checkout"]

    price = create_price(id, room, adult, child, days)

    hotel = Hotel.objects.get(id=id)
    return render(request, "book/book.html" , {
        "price": price,
        "hotel": hotel,
        "room": room,
        "adult": adult,
        "child": child,
        "checkin": checkin,
        "checkout": checkout,
        "days": days,
    })

def successful(request):
    if request.method != "POST":
        return render(request, "book/apology.html", {
            "message": "Error occured"
        })

    id = int(request.POST["id"])
    hotel = Hotel.objects.get(id=id)
    checkin = request.POST["checkin"]
    checkout = request.POST["checkout"]

    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    phone = request.POST["phone"]
    email = request.POST["email"]

    room = int(request.POST["room"])
    adult = int(request.POST["adult"])
    child = int(request.POST["child"])
    days = int(request.POST["days"])

    price = str(create_price(id, room, adult, child, days))

    tracking_id = first_name[0] + last_name[0] + str(int(time.time()))
    print(tracking_id)

    b = Booking(
        hotel=hotel,
        checkin_date=checkin,
        checkout_date=checkout,
        room=room,
        adult=adult,
        child=child,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        tracking_id=tracking_id,
        price=price
    )

    try:
        b.save()
    except:
        print("Error Occured")
        return render(request, "book/apology.html", {
            "message": "Internal Server Error"
        })

    MERCHANT_KEY = 'q39E3lhdMhhbL5FZ'
    data_dict = {
            'MID':'ILTgFX19787861166187',
            'ORDER_ID':tracking_id,
            'TXN_AMOUNT':price,
            'CUST_ID':email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'webstaging',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/callback',
        }

    param_dict = data_dict
    param_dict['CHECKSUMHASH'] =Checksum.generate_checksum(data_dict, MERCHANT_KEY)

    return render(request, "book/paytm.html", {
        "param_dict": param_dict
    })


@csrf_exempt
def callback(request):
    if request.method == "POST":
        tracking_id = request.POST["ORDERID"]
        print(request.POST)
        return render(request, "book/successful.html", {
        "tracking_id": tracking_id
    })
    # paytm callback
    print(request.GET)
    return render(request, "book/apology.html", {
        "message": "Order failed due to some reason"
    })
    

def track_booking(request):
    if request.method=="POST":
        tracking_id = request.POST["tracking-id"]
        phone = request.POST["phone"]
        try:
            booking = Booking.objects.get(tracking_id=tracking_id, phone=phone)
            return render(request, "book/track.html", {
                "booking": booking
            })

        except:
            return render(request, "book/track.html", {
                "message": "Invalid tracking ID"
            })

    return render(request, "book/track.html")


@login_required(login_url="login")
def profile(request):
    return render(request, "book/profile.html")

def login_view(request):
    if request.user.is_authenticated:
        return render(request, "book/apology.html", {
            "message": "Already logged in"
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
            return render(request, "book/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "book/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.user.is_authenticated:
        return render(request, "book/apology.html", {
            "message": "Already logged in"
        })
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        phone = int(request.POST["phone"])

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "book/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "book/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "book/register.html")

from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Cart, Order

# Create your views here.


def index(req):
    username = req.user.username
    allproducts = Product.objects.all()
    context = {"username": username, "allproducts": allproducts}
    return render(req, "index.html", context)


def userlogout(req):
    logout(req)
    return redirect("/")


def loginuser(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" or upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "loginuser.html", context)
        else:
            username = uname
            userdata = authenticate(username=uname, password=upass)
            context = {"username": username}
            if userdata is not None:
                login(req, userdata)
                # return redirect("/")
                return render(req, "index.html", context)
            else:
                context["errmsg"] = "Invalid username and password"
                return render(req, "loginuser.html", context)
    else:
        return render(req, "loginuser.html")


def registeruser(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "registeruser.html", context)
        elif upass != ucpass:
            context["errmsg"] = "Password and Confirm Password doesn't match"
            return render(req, "registeruser.html", context)
        else:
            try:
                userdata = User.objects.create(username=uname, password=upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("/")
            except Exception:
                context["errmsg"] = "User Already Exists"
                return render(req, "registeruser.html", context)
    else:
        return render(req, "registeruser.html")


def aboutus(req):
    return render(req, "aboutus.html")


def contactus(req):
    return render(req, "contactus.html")


def mobilelistview(req):
    if req.method == "GET":
        allproducts = Product.prod.mobile_list()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)


def clothslistview(req):
    if req.method == "GET":
        allproducts = Product.prod.cloths_list()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)


def shoeslistview(req):
    if req.method == "GET":
        allproducts = Product.prod.shoes_list()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    else:
        allproducts = Product.objects.all()
        context = {"allproducts": allproducts}
        return render(req, "index.html", context)
    

def range_view(req):
    if req.method == "GET":
        return render(req, 'index.html')
    else:
        r1 = req.POST.get('min')
        r2 = req.POST.get('max')
        if r1 is not None and r2 is not None and r1.isdigit() and r2.isdigit():
            allproducts = Product.prod.get_price_range(r1, r2)
            context = {"allproducts": allproducts}
            return render(req, "index.html", context)
        else:
            allproducts = Product.objects.all()
            context = {"allproducts": allproducts}
            return render(req, "index.html", context)


def allsortedorderview(req):
    sort_option = req.GET.get("sort")
    if sort_option == "high_to_low":
        allproducts = Product.objects.order_by("-price")
    elif sort_option == "low_to_high":
        allproducts = Product.objects.order_by("price")
    else:
        allproducts = Product.objects.all()
    
    context = {'allproducts': allproducts}
    return render(req, 'index.html', context)


from django.db.models import Q

def searchproduct(req):
    query = req.GET.get("q")
    if query:
        allproducts = Product.objects.filter(
            Q(product_name__icontains = query)
            |Q(category__icontains = query)
            |Q(price__icontains = query)
            |Q(desc__icontains = query)
        )
    else:
        allproducts = Product.objects.all()
    context = {"allproducts":allproducts, "query":query}
    return render(req, "index.html", context)
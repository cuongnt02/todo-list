from django.http import HttpRequest
from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request: HttpRequest):
    return render(request, "home.html")


def view_list(request: HttpRequest):
    items = Item.objects.all()
    return render(request, "list.html", {"items": items})


def new_list(request: HttpRequest):
    nulist = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=nulist)
    return redirect("/lists/the-only-list-in-the-world/")

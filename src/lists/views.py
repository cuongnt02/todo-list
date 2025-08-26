from django.http import HttpRequest
from django.shortcuts import render, redirect
from lists.models import Item, List


def home_page(request: HttpRequest):
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id):
    our_list = List.objects.get(id=list_id)
    items = Item.objects.filter(list=our_list)
    return render(request, "list.html", {"list": our_list})


def add_item(request: HttpRequest, list_id):
    our_list = List.objects.get(id=list_id)
    item = Item.objects.create(text=request.POST["item_text"], list=our_list)
    return redirect(f"/lists/{our_list.id}/")


def new_list(request: HttpRequest):
    nulist = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=nulist)
    return redirect(f"/lists/{nulist.id}/")

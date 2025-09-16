from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers

from main.models import Product
from main.forms import ProductForm
 

# --- Main page: list all products ---
def show_main(request):
    products = Product.objects.all()
    context = {
        "npm": "2406495956",       # change to your real NPM
        "name": "Cristian Dillon Philbert",      # change to your real name
        "class": "PBP A",         # change if needed
        "products": products,
    }
    return render(request, "main.html", context)


# --- Add new product via form ---
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:show_main")

    return render(request, "create_product.html", {"form": form})


# --- Detail page for a product ---
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {"product": product})


# --- Data delivery views (Assignment 3 requirement) ---

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml"
    )

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(
        serializers.serialize("json", data),
        content_type="application/json"
    )

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml"
    )

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("json", data),
        content_type="application/json"
    )

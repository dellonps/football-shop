import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.models import Product
from main.forms import ProductForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.forms.models import model_to_dict
import requests
import json
import base64



 

@login_required(login_url="/login")
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'
    category_filter = request.GET.get("category", None)

    if filter_type == "all":
        shop_list = Product.objects.all()
    else:
        shop_list = Product.objects.filter(user=request.user)

    categories = Product.objects.values_list("category", flat=True).distinct()
    if category_filter:
        shop_list = shop_list.filter(category=category_filter)

    menu_items = [('all', 'All Products'), ('my', 'My Products')]

    context = {
        "npm": "2406495956",
        "name": "Cristian Dillon Philbert",
        "class": "PBP A",
        "products": shop_list,
        "categories": categories,
        "last_login": request.COOKIES.get('last_login', 'Never'),
        "menu_items": menu_items,
    }
    return render(request, "main.html", context)


@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        shop_entry = form.save(commit = False)
        shop_entry.user = request.user
        shop_entry.save()
        return redirect('main:show_main')
        
    context = {
        'form': form
    }


    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {"product": product})

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))


def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response




def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)





# --- AJAX Endpoints ---
@csrf_exempt
@require_POST
@login_required
def add_product_ajax(request):
    form = ProductForm(request.POST)
    if form.is_valid():
        # Create the product from cleaned data, ensuring security and correctness
        product = form.save(commit=False)
        product.user = request.user
        # Apply strip_tags to the specific fields
        product.name = strip_tags(form.cleaned_data.get("name"))
        product.description = strip_tags(form.cleaned_data.get("description"))
        product.save()

        # Return JSON data
        data = {
            'pk': product.pk,
            'fields': {
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'category': product.category,
                'thumbnail': product.thumbnail,
                'user': product.user.id,
            }
        }
        return JsonResponse(data, status=201)
    else:
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)




@csrf_exempt
@require_POST
@login_required
def edit_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id, user=request.user)
    form = ProductForm(request.POST, instance=product)
    if form.is_valid():
        # Save the form with the updated data
        product = form.save(commit=False)
        # Apply strip_tags to the specific fields
        product.name = strip_tags(form.cleaned_data.get("name"))
        product.description = strip_tags(form.cleaned_data.get("description"))
        product.save()
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)

@csrf_exempt
@require_POST
def delete_product_ajax(request, id):
    # Ensure the user is authenticated (login_required normally handles redirects,
    # but for AJAX we explicitly return JSON status codes so frontend can react)
    if not request.user or not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required."}, status=401)

    try:
        print(f"delete_product_ajax called: user={getattr(request.user, 'username', None)} id={id}")
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found."}, status=404)

    # Ownership check
    if product.user_id != request.user.id:
        print(f"delete_product_ajax denied: user={getattr(request.user, 'username', None)} not owner of product id={id} (owner_id={product.user_id})")
        return JsonResponse({"status": "error", "message": "Permission denied. Only owner can delete this product."}, status=403)

    # Delete and return success
    product.delete()
    print(f"delete_product_ajax success: product id={id} deleted by user={getattr(request.user, 'username', None)}")
    return JsonResponse({"status": "success"}, status=200)



@csrf_exempt
@require_POST
def login_ajax(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = JsonResponse({"status": "success", "message": "Login successful!"})
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
    else:
        return JsonResponse({"status": "error", "message": "Invalid username or password."}, status=401)

@csrf_exempt
@require_POST
def register_ajax(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success", "message": "Registration successful! You can now log in."}, status=201)
    else:
        return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@login_required
def get_products_json(request):
    filter_type = request.GET.get("filter")
    if filter_type == "my":
        products = Product.objects.filter(user=request.user)
    else:
        products = Product.objects.all()
    return HttpResponse(serializers.serialize("json", products), content_type="application/json")

@login_required
def get_product_by_id_json(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return JsonResponse(model_to_dict(product))










def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml"
    )

@login_required
def show_json(request):
    filter_type = request.GET.get("filter", "all")

    if filter_type == "all":
        product_list = Product.objects.all()
    elif filter_type == "my":
        product_list = Product.objects.filter(user=request.user)
    else:
        category = request.GET.get("category")
        if category:
            product_list = Product.objects.filter(category=category)
        else:
            product_list = Product.objects.all()

    json_data = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'user_username': product.user.username if product.user else None,
        }
        for product in product_list
    ]
    return JsonResponse(json_data, safe=False)


def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml"
    )

def show_json_by_id(request, id):
    try:
        product = Product.objects.select_related('user').get(pk=id)
        data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,  # kalau DecimalField
            'thumbnail': product.thumbnail,
            'user_id': product.user.id,
            'user_username': product.user.username if product.user else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def proxy_image(request):
    image_url = request.GET.get('url')
    if not image_url:
        return HttpResponse('No URL provided', status=400)
    
    if image_url.startswith("data:image"):
        try:
            header, b64data = image_url.split(",", 1)

            # Ambil MIME type: contoh "image/jpeg"
            mime = header.split(";")[0].split(":")[1]  

            # Decode base64 → bytes
            image_data = base64.b64decode(b64data)

            return HttpResponse(image_data, content_type=mime)

        except Exception as e:
            return HttpResponse(f'Error decoding base64 image: {str(e)}', status=500)
    try:
        # Fetch image from external source
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Return the image with proper content type
        return HttpResponse(
            response.content,
            content_type=response.headers.get('Content-Type', 'image/jpeg')
        )
    except requests.RequestException as e:
        return HttpResponse(f'Error fetching image: {str(e)}', status=500)
    

@csrf_exempt
@login_required
def create_product_flutter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = strip_tags(data.get("name", ""))  # Strip HTML tags
        description = strip_tags(data.get("description", ""))  # Strip HTML tags
        category = data.get("category", "")
        thumbnail = data.get("thumbnail", "")
        price_raw = data.get("price", 0)
        user = request.user
        try:
            # sesuaikan dengan tipe di models.py (IntegerField / FloatField / DecimalField)
            price = int(price_raw)
        except (TypeError, ValueError):
            return JsonResponse(
                {"status": "error", "message": "Price must be a valid number"},
                status=400
            )
        

        
        new_product = Product(
            name= name, 
            description=description,
            category=category,
            thumbnail=thumbnail,
            user=user,
            price=price,
        )
        new_product.save()
        
        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@login_required
def show_my_products_json(request):
    products = Product.objects.filter(user=request.user).order_by("-created_at")
    data = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "category": p.category,
            "thumbnail": p.thumbnail,
            "created_at": p.created_at.isoformat(),
        }
        for p in products
    ]
    return JsonResponse(data, safe=False)
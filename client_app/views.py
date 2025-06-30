from django.http import HttpResponse, HttpResponseForbidden
from .models import Product, Category, CartItem, User_details, Order
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Orders_detail
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token





@login_required
def dashboard(request):
    if not request.user.is_staff:
        return render(request, 'access_denied.html')  # 🔒 Show error for normal users

    # Dashboard logic
    selected_category = request.GET.get('category_id')
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', '')  
    products = Product.objects.all()
    if selected_category:
        products = products.filter(categ__id=selected_category)
    if search_query:
        products = products.filter(name__icontains=search_query)
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    categories = Category.objects.all()
    orders = Order.objects.all()
    users = User.objects.all()

    return render(request, 'dashboard.html', {
        'orders': orders,
        'users': users,
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by, 
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect admin users to dashboard
            if user.is_staff or user.is_superuser:
                return redirect('dashboard')
            # Redirect normal users to home
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            next_url = request.POST.get('next', '')
            return render(request, "login.html", {'next': next_url})
    # ADD THIS FOR GET REQUESTS:
    next_url = request.GET.get('next', '')
    return render(request, "login.html", {'next': next_url})
  


def add_product(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        pname = request.POST.get('name')
        pr = request.POST.get('price')
        pstock = request.POST.get('stock')
        cat_id = request.POST.get('categ')
        description = request.POST.get('description')
        productimage = request.FILES.get('image')

        if not all([pname, pr, pstock, cat_id, productimage]):
            return HttpResponse("Please fill in all fields and upload an image.")

        try:
            catobj = Category.objects.get(id=cat_id)
        except Category.DoesNotExist:
            return HttpResponse("Selected category does not exist.")

        Product.objects.create(
            name=pname,
            price=pr,
            stock=pstock,
            product_image=productimage,
            categ=catobj,
            description=description
        )
        return HttpResponse("Product added successfully")

    return render(request, "add_product.html", {'categories': categories})

def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        return HttpResponse("User created successfully")
    return render(request, "sign_up.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def home(request):
    category_id = request.GET.get('category_id')
    if category_id:
        products = Product.objects.filter(categ__id=category_id)
    else:
        products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})



@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def add_to_cart(request, product_id):
    prod = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=prod)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    prod = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(user=request.user, product=prod).delete()
    return redirect('cart')

def buy_now(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.warning(request, "Your cart is empty!")
            return redirect('cart')
        # Save order details to DB here (not implemented)
        request.session['cart'] = {}
        messages.success(request, "Purchase successful! Thank you for shopping.")
        return redirect('home')
    else:
        return redirect('cart')

def admin_dashboard(request):
    users = User.objects.all()
    products = Product.objects.all()
    return render(request, 'admin.html', {'users': users, 'products': products})

def edit_product(request, product_id):
    product_obj = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        product_obj.name = request.POST.get('name')
        product_obj.price = request.POST.get('price')
        product_obj.stock = request.POST.get('stock')
        cat_id = request.POST.get('categ')
        product_obj.categ = get_object_or_404(Category, id=cat_id)
        if request.FILES.get('image'):
            product_obj.product_image = request.FILES['image']
        product_obj.description = request.POST.get('description')
        product_obj.save()
        return redirect('dashboard')
    return render(request, 'edit_product.html', {'product': product_obj, 'categories': categories})

def delete_product(request, product_id):
    product_obj = get_object_or_404(Product, id=product_id)
    product_obj.delete()
    return redirect('dashboard')

def product_detail(request, product_id):
    product_obj = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product_obj})

@login_required
def order_page(request, product_id):
    cart_item = get_object_or_404(CartItem, user=request.user, product_id=product_id)
    product = cart_item.product
    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')
        quantity = cart_item.quantity

        # Check if enough stock is available
        if product.stock < quantity:
            messages.error(request, "Not enough stock available.")
            return redirect('cart')

        # Decrease stock
        product.stock -= quantity
        product.save()

        Orders_detail.objects.create(
            user=request.user,
            address=address,
            payment_method=payment_method
        )
        cart_item.delete()
        return render(request, 'order_success.html')
    return render(request, 'order_page.html', {
        'cart_item': cart_item,
        'total': cart_item.subtotal,
    })
def product_filter(request):
    if request.method == 'POST':
        pname = request.POST.get('name', '')
        if pname:
            products = Product.objects.filter(name__icontains=pname)
        else:
            products = Product.objects.all()
        return render(request, 'home.html', {'products': products})
    return redirect('home')

@login_required
def orders_detail(request):
    orders = Orders_detail.objects.all().order_by('-id')  # or filter by user if needed
    return render(request, 'orders_detail.html', {'orders': orders})

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from .models import Orders_detail

@login_required
def approve_order(request, order_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to approve orders.")
    order = get_object_or_404(Orders_detail, id=order_id)
    if request.method == 'POST':
        order.status = 'approved'
        order.save()
    return redirect('orders_detail')  # or 'dashboard' if that's your admin page

@login_required
def my_orders(request):
    orders = Orders_detail.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})


#rest api views
@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def get_user_details(request):
    user_data=User.objects.all()
    serializer = User_detailsSerializer(user_data, many=True)
    return Response(serializer.data)

@api_view(['GET' ,'POST'])
def post_user_details(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        return Response(" success")
    return Response("please respond to the form...")

#api update

@api_view(['PUT','GET'])
def update_user_details(request, user_id):
    user = User.objects.filter(id=user_id)
    if request.method == 'PUT':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user.update(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        return Response("User details updated successfully")
    return Response("Please respond to the form...")





@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=200)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_protected_view(request):
    # Only accessible with a valid JWT token
    return Response({"message": "This is a protected view."})
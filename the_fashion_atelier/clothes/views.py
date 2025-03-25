from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Avg
from django.urls import reverse
from .models import Clothing, CartItem, Order, OrderItem, UserProfile, Review, Product, Category
from .forms import RegistrationForm, UserProfileForm, LoginForm, CheckoutForm, PaymentForm, CartItemForm
from django.core.paginator import Paginator
import random
from django.utils import timezone

def home(request):
    try:
        featured_products = list(Product.objects.filter(is_featured=True)[:4])
        categories = list(Category.objects.all())
        
        # Debug information
        print(f"Featured products count: {len(featured_products)}")
        if featured_products:
            for p in featured_products:
                print(f"Product: {p.name}, Image: {p.image if hasattr(p, 'image') else 'No image'}")
        
        return render(request, 'clothes/home.html', {
            'featured_products': featured_products,
            'categories': categories
        })
    except Exception as e:
        print(f"Error in home view: {e}")
        # Return a minimal response to avoid breaking the site
        return render(request, 'clothes/home.html', {
            'featured_products': [],
            'categories': []
        })

def products(request):
    products_list = Product.objects.all()
    categories = Category.objects.all()
    
    # Filtering
    category_id = request.GET.get('category')
    if category_id:
        products_list = products_list.filter(category_id=category_id)
    
    # Sorting
    sort = request.GET.get('sort')
    if sort:
        if sort == 'price-asc':
            products_list = products_list.order_by('price')
        elif sort == 'price-desc':
            products_list = products_list.order_by('-price')
        elif sort == 'name-asc':
            products_list = products_list.order_by('name')
        elif sort == 'name-desc':
            products_list = products_list.order_by('-name')
    
    # Pagination
    paginator = Paginator(products_list, 9)  # 9 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request, 'clothes/products.html', {
        'products': products,
        'categories': categories
    })

def about(request):
    return render(request, 'clothes/about.html')

def contact(request):
    return render(request, 'clothes/contact.html')

def men_clothes(request):
    query = request.GET.get('q', '')
    men_items = Clothing.objects.filter(category='men')
    
    if query:
        men_items = men_items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'clothes/clothes_list.html', {
        'items': men_items,
        'category': 'Men',
        'title': 'SC - Men\'s Collection',
        'search_query': query
    })

def women_clothes(request):
    query = request.GET.get('q', '')
    women_items = Clothing.objects.filter(category='women')
    
    if query:
        women_items = women_items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'clothes/clothes_list.html', {
        'items': women_items,
        'category': 'Women',
        'title': 'SC - Women\'s Collection',
        'search_query': query
    })

def all_products(request):
    query = request.GET.get('q', '')
    items = Clothing.objects.all()
    
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    return render(request, 'clothes/clothes_list.html', {
        'items': items,
        'category': 'All',
        'title': 'SC - All Products',
        'search_query': query
    })

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    
    # Get related products (same category, exclude current product)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    
    return render(request, 'clothes/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            # Log the user in
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            
            messages.success(request, "Registration successful!")
            return redirect('clothes:home')
    else:
        user_form = RegistrationForm()
        profile_form = UserProfileForm()
    
    return render(request, 'clothes/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'title': 'SC - Register'
    })

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('clothes:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'clothes/login.html', {
        'form': form,
        'title': 'SC - Login'
    })

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('clothes:home')

@login_required
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('clothes:user_profile')
    else:
        user_form = RegistrationForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    return render(request, 'clothes/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'clothes/orders.html', {'orders': orders})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size', 'M')
    quantity = int(request.POST.get('quantity', 1))
    
    # Get or create cart for the current user
    cart_items = request.session.get('cart_items', [])
    
    # Check if product already exists in cart
    item_exists = False
    for item in cart_items:
        if item['product_id'] == product_id and item['size'] == size:
            item['quantity'] += quantity
            item_exists = True
            break
    
    if not item_exists:
        cart_items.append({
            'product_id': product_id,
            'size': size,
            'quantity': quantity,
            'price': float(product.price)
        })
    
    request.session['cart_items'] = cart_items
    messages.success(request, f'{product.name} added to your cart!')
    
    return redirect('clothes:cart')

def cart(request):
    cart_items = request.session.get('cart_items', [])
    
    # Get actual product objects
    items = []
    subtotal = 0
    for item in cart_items:
        product = get_object_or_404(Product, id=item['product_id'])
        item_total = float(product.price) * item['quantity']
        subtotal += item_total
        items.append({
            'id': len(items),  # Use index as ID for cart operations
            'product': product,
            'size': item['size'],
            'quantity': item['quantity'],
            'total': item_total
        })
    
    # Calculate shipping and total
    shipping = 4.99 if subtotal > 0 and subtotal < 100 else 0
    discount = 0  # Can be calculated based on promo codes
    total = subtotal + shipping - discount
    
    context = {
        'cart_items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'discount': discount,
        'total': total
    }
    
    return render(request, 'clothes/cart.html', context)

def update_cart(request, item_id):
    cart_items = request.session.get('cart_items', [])
    quantity = int(request.POST.get('quantity', 1))
    
    if 0 <= item_id < len(cart_items):
        cart_items[item_id]['quantity'] = quantity
        request.session['cart_items'] = cart_items
    
    return redirect('clothes:cart')

def remove_from_cart(request, item_id):
    cart_items = request.session.get('cart_items', [])
    
    if 0 <= item_id < len(cart_items):
        cart_items.pop(item_id)
        request.session['cart_items'] = cart_items
    
    return redirect('clothes:cart')

def apply_promo(request):
    # Simple implementation for demo purposes
    promo_code = request.POST.get('promo_code', '').upper()
    
    if promo_code == 'WELCOME10':
        messages.success(request, 'Promo code WELCOME10 applied for 10% discount!')
        request.session['discount'] = 10
    elif promo_code == 'FREESHIP':
        messages.success(request, 'Promo code FREESHIP applied for free shipping!')
        request.session['free_shipping'] = True
    else:
        messages.error(request, 'Invalid promo code.')
    
    return redirect('clothes:cart')

def checkout(request):
    cart_items = request.session.get('cart_items', [])
    
    if not cart_items:
        messages.warning(request, 'Your cart is empty. Add some products before checkout.')
        return redirect('clothes:products')
    
    # Get actual product objects
    items = []
    subtotal = 0
    for item in cart_items:
        product = get_object_or_404(Product, id=item['product_id'])
        item_total = float(product.price) * item['quantity']
        subtotal += item_total
        items.append({
            'id': len(items),
            'product': product,
            'size': item['size'],
            'quantity': item['quantity'],
            'total': item_total
        })
    
    # Calculate shipping and total
    shipping = 4.99 if subtotal > 0 and subtotal < 100 else 0
    discount = 0  # Can be calculated based on promo codes
    total = subtotal + shipping - discount
    
    context = {
        'cart_items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'discount': discount,
        'total': total
    }
    
    return render(request, 'clothes/checkout.html', context)

def payment(request):
    return render(request, 'clothes/payment.html')

def order_confirmation(request):
    # In a real application, you would create and save an Order object
    # Here we'll just simulate an order with the cart data
    cart_items = request.session.get('cart_items', [])
    
    if not cart_items:
        return redirect('clothes:home')
    
    # Create mock order data
    order = {
        'order_number': f"ORD-{random.randint(100000, 999999)}",
        'created_at': timezone.now(),
        'first_name': 'John',  # In real app, get from form
        'last_name': 'Doe',    # In real app, get from form
        'email': 'john.doe@example.com',  # In real app, get from form
        'address': '123 Fashion St',      # In real app, get from form
        'city': 'London',                 # In real app, get from form
        'postcode': 'SW1A 1AA',           # In real app, get from form
        'country': 'United Kingdom',      # In real app, get from form
        'shipping_method_display': 'Standard Shipping (3-5 business days)',
        'estimated_delivery': timezone.now() + timezone.timedelta(days=5),
    }
    
    # Get actual product objects
    items = []
    subtotal = 0
    for item in cart_items:
        product = get_object_or_404(Product, id=item['product_id'])
        item_total = float(product.price) * item['quantity']
        subtotal += item_total
        items.append({
            'product': product,
            'quantity': item['quantity'],
            'price': float(product.price),
            'total': item_total
        })
    
    # Calculate shipping and total
    shipping = 4.99 if subtotal > 0 and subtotal < 100 else 0
    discount = 0  # Can be calculated based on promo codes
    total = subtotal + shipping - discount
    
    # Add totals to order
    order['subtotal'] = subtotal
    order['shipping'] = shipping
    order['discount'] = discount
    order['total'] = total
    
    # Clear cart after successful order
    request.session['cart_items'] = []
    
    context = {
        'order': order,
        'order_items': items
    }
    
    return render(request, 'clothes/order_confirmation.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'clothes/order_history.html', {
        'orders': orders,
        'title': 'SC - Order History'
    })

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    
    return render(request, 'clothes/order_detail.html', {
        'order': order,
        'order_items': order_items,
        'title': f'SC - Order #{order.id}'
    })

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Clothing, id=product_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        
        # Check if user already has a review for this product
        review, created = Review.objects.get_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if not created:
            # Update existing review
            review.rating = rating
            review.comment = comment
            review.save()
            messages.success(request, 'Your review has been updated!')
        else:
            messages.success(request, 'Your review has been added!')
            
        return redirect('clothes:product_detail', product_id=product_id)
    
    return redirect('clothes:product_detail', product_id=product_id)

def clothing_detail(request, clothing_id):
    clothing = get_object_or_404(Clothing, id=clothing_id)
    
    # Get related clothing items (same category)
    related_items = Clothing.objects.filter(category=clothing.category).exclude(id=clothing.id)[:4]
    
    return render(request, 'clothes/clothing_detail.html', {
        'clothing': clothing,
        'related_items': related_items
    })

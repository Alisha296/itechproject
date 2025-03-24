from django.urls import path
from . import views

app_name = 'clothes'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('men/', views.men_clothes, name='men'),
    path('women/', views.women_clothes, name='women'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('clothing/<int:clothing_id>/', views.clothing_detail, name='clothing_detail'),
    path('products/<int:product_id>/review/', views.add_review, name='add_review'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # Cart URLs
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('apply-promo/', views.apply_promo, name='apply_promo'),
    
    # Checkout and Payment URLs
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    
    # Order History URLs
    path('order-history/', views.order_history, name='order_history'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # User account URLs
    path('orders/', views.user_orders, name='user_orders'),
] 
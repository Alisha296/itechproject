from django.contrib import admin
from .models import Clothing, CartItem, Order, OrderItem, UserProfile, Review, Category, Product

@admin.register(Clothing)
class ClothingAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'availability_status')
    list_filter = ('category', 'availability_status')
    search_fields = ('name', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user__username', 'product__name')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'clothing', 'quantity', 'size', 'color', 'added_at')
    list_filter = ('added_at', 'size', 'color')
    search_fields = ('user__username', 'clothing__name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'status', 'payment_method', 'payment_completed', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_completed', 'created_at')
    search_fields = ('user__username', 'full_name', 'email')
    inlines = [OrderItemInline]

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'state')
    search_fields = ('user__username', 'phone', 'city')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount', 'is_featured', 'is_new', 'stock')
    list_filter = ('category', 'is_featured', 'is_new')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'discount', 'is_featured', 'is_new', 'stock')

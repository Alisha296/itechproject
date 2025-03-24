import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypro.settings')
django.setup()

# Now we can import our models
from clothes.models import Category, Product
from django.core.files.uploadedfile import SimpleUploadedFile
import random
import shutil
import urllib.request
from urllib.error import URLError
import ssl

def download_image(url, filename):
    """Download an image from a URL to the media directory"""
    try:
        # Ignore SSL certificate validation
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(url, context=context) as response, open(filename, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return True
    except URLError as e:
        print(f"Error downloading {url}: {e}")
        return False

def create_sample_data():
    """Create sample categories and products"""
    
    # Category data
    categories_data = [
        {
            'name': 'Men',
            'description': 'Fashion for men including shirts, trousers, and accessories.',
            'image_url': 'https://images.unsplash.com/photo-1516257984-b1b4d707412e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
        },
        {
            'name': 'Women',
            'description': 'Latest women\'s fashion including dresses, tops, and accessories.',
            'image_url': 'https://images.unsplash.com/photo-1483985988355-763728e1935b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
        },
        {
            'name': 'Accessories',
            'description': 'Complete your look with our stylish accessories.',
            'image_url': 'https://images.unsplash.com/photo-1511556532299-8f662fc26c06?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
        },
    ]
    
    categories = []
    
    # Create categories
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
            }
        )
        
        # Download and set image
        if created or not category.image:
            img_path = f"media/categories/{category.slug}.jpg"
            if download_image(cat_data['image_url'], img_path):
                category.image = f"categories/{category.slug}.jpg"
                category.save()
        
        categories.append(category)
    
    # Product data
    products_data = [
        # Men's products
        {
            'name': 'Classic Oxford Shirt',
            'description': 'A timeless Oxford shirt perfect for any occasion. Made from 100% cotton for comfort and durability.',
            'price': 59.99,
            'discount': 0,
            'category': 'Men',
            'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_featured': True,
            'is_new': True,
            'stock': 25,
        },
        {
            'name': 'Slim Fit Chinos',
            'description': 'Modern slim fit chinos that offer both style and comfort. Perfect for casual or smart casual wear.',
            'price': 49.99,
            'discount': 10,
            'category': 'Men',
            'image_url': 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_featured': False,
            'is_new': True,
            'stock': 20,
        },
        {
            'name': 'Classic Denim Jacket',
            'description': 'A versatile denim jacket that never goes out of style. Features a comfortable fit and durable construction.',
            'price': 89.99,
            'discount': 0,
            'category': 'Men',
            'image_url': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_featured': True,
            'is_new': False,
            'stock': 15,
        },
        
        # Women's products
        {
            'name': 'Floral Summer Dress',
            'description': 'A beautiful floral dress perfect for summer days. Made from lightweight fabric for maximum comfort.',
            'price': 79.99,
            'discount': 15,
            'category': 'Women',
            'image_url': 'https://images.unsplash.com/photo-1492707892479-7bc8d5a4ee93?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_featured': True,
            'is_new': True,
            'stock': 18,
        },
        {
            'name': 'High-Waisted Jeans',
            'description': 'Stylish high-waisted jeans with a modern fit. Made from premium denim for comfort and durability.',
            'price': 69.99,
            'discount': 0,
            'category': 'Women',
            'image_url': 'https://images.unsplash.com/photo-1475178626620-a4d074967452?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_featured': False,
            'is_new': True,
            'stock': 22,
        },
        {
            'name': 'Elegant Silk Blouse',
            'description': 'A luxurious silk blouse perfect for both office wear and special occasions.',
            'price': 99.99,
            'discount': 5,
            'category': 'Women',
            'image_url': 'https://images.unsplash.com/photo-1533659828870-95ee305cee3e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_featured': True,
            'is_new': False,
            'stock': 12,
        },
        
        # Accessories
        {
            'name': 'Leather Watch',
            'description': 'A classic leather watch that adds sophistication to any outfit. Features precision quartz movement.',
            'price': 129.99,
            'discount': 0,
            'category': 'Accessories',
            'image_url': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_featured': True,
            'is_new': True,
            'stock': 10,
        },
        {
            'name': 'Premium Leather Belt',
            'description': 'A high-quality leather belt finished with a classic buckle. Perfect for both casual and formal wear.',
            'price': 49.99,
            'discount': 0,
            'category': 'Accessories',
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_featured': False,
            'is_new': True,
            'stock': 15,
        },
        {
            'name': 'Designer Sunglasses',
            'description': 'Stylish sunglasses with UV protection. Lightweight frame and modern design.',
            'price': 89.99,
            'discount': 10,
            'category': 'Accessories',
            'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
            'is_featured': True,
            'is_new': False,
            'stock': 8,
        },
    ]
    
    # Create products
    for prod_data in products_data:
        # Find the category
        category = Category.objects.get(name=prod_data['category'])
        
        product, created = Product.objects.get_or_create(
            name=prod_data['name'],
            defaults={
                'description': prod_data['description'],
                'price': prod_data['price'],
                'discount': prod_data['discount'],
                'category': category,
                'is_featured': prod_data['is_featured'],
                'is_new': prod_data['is_new'],
                'stock': prod_data['stock'],
            }
        )
        
        # Download and set image
        if created or not product.image:
            img_path = f"media/products/{product.slug}.jpg"
            if download_image(prod_data['image_url'], img_path):
                product.image = f"products/{product.slug}.jpg"
                product.save()

if __name__ == '__main__':
    print("Creating sample data...")
    create_sample_data()
    print("Sample data created successfully!") 
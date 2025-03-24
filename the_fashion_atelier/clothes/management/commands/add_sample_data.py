from django.core.management.base import BaseCommand
from clothes.models import Clothing, Review
from django.contrib.auth.models import User
from django.db import transaction
import random

class Command(BaseCommand):
    help = 'Adds sample clothing data to the database'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # Clear existing clothing data
        self.stdout.write('Clearing existing clothing data...')
        Clothing.objects.all().delete()
        Review.objects.all().delete()

        # Sample clothing data
        clothing_data = [
            # Men's clothing
            {
                'name': 'Classic Blue Shirt',
                'description': 'A timeless blue button-up shirt perfect for any occasion. Made from 100% cotton for comfort and durability.',
                'price': 39.99,
                'category': 'men',
                'image_url': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80',
                'available_sizes': 'S,M,L,XL,XXL',
                'available_colors': 'Blue,White,Black',
                'availability_status': 'in_stock',
            },
            {
                'name': 'Slim Fit Black Pants',
                'description': 'Modern slim fit pants in classic black. Features stretch fabric for comfort and mobility.',
                'price': 49.99,
                'category': 'men',
                'image_url': 'https://images.unsplash.com/photo-1473966968600-fa801b869a1a?ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80',
                'available_sizes': '30,32,34,36,38',
                'available_colors': 'Black,Navy,Grey',
                'availability_status': 'in_stock',
            },
            {
                'name': 'Casual Denim Jacket',
                'description': 'A versatile denim jacket that works with any outfit. Features classic styling with modern details.',
                'price': 59.99,
                'category': 'men',
                'image_url': 'https://images.unsplash.com/photo-1576871337622-98d48d1cf531?ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80',
                'available_sizes': 'S,M,L,XL',
                'available_colors': 'Blue,Light Blue,Dark Blue',
                'availability_status': 'low_stock',
            },
            {
                'name': 'Premium Cotton T-Shirt',
                'description': 'Ultra-soft premium cotton t-shirt with a relaxed fit. Available in multiple colors.',
                'price': 24.99,
                'category': 'men',
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80',
                'available_sizes': 'S,M,L,XL,XXL',
                'available_colors': 'White,Black,Grey,Navy,Red',
                'availability_status': 'in_stock',
            },
            {
                'name': 'Wool Blend Sweater',
                'description': 'Warm and comfortable wool blend sweater, perfect for colder weather. Features ribbed cuffs and hem.',
                'price': 69.99,
                'category': 'men',
                'image_url': 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80',
                'available_sizes': 'M,L,XL',
                'available_colors': 'Grey,Navy,Burgundy',
                'availability_status': 'out_of_stock',
            },
            
            # Women's clothing
            {
                'name': 'Floral Print Dress',
                'description': 'Beautiful floral print dress with a flattering silhouette. Perfect for spring and summer occasions.',
                'price': 79.99,
                'category': 'women',
                'image_url': 'https://images.unsplash.com/photo-1582533561751-ef6f6ab93a2e?ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80',
                'available_sizes': 'XS,S,M,L',
                'available_colors': 'Floral Blue,Floral Pink',
                'availability_status': 'in_stock',
            },
            {
                'name': 'High-Waisted Jeans',
                'description': 'Classic high-waisted jeans with a modern fit. Made from premium denim with just the right amount of stretch.',
                'price': 59.99,
                'category': 'women',
                'image_url': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80',
                'available_sizes': '26,27,28,29,30,31,32',
                'available_colors': 'Blue,Dark Blue,Black',
                'availability_status': 'in_stock',
            },
            {
                'name': 'Silk Blouse',
                'description': 'Elegant silk blouse that transitions effortlessly from work to evening. Features a timeless design.',
                'price': 89.99,
                'category': 'women',
                'image_url': 'https://images.unsplash.com/photo-1604575228217-1751e15d45ab?ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80',
                'available_sizes': 'XS,S,M,L',
                'available_colors': 'White,Cream,Black,Pink',
                'availability_status': 'low_stock',
            },
            {
                'name': 'Leather Jacket',
                'description': 'Premium leather jacket with a flattering cut. Fully lined with multiple pockets and silver hardware.',
                'price': 149.99,
                'category': 'women',
                'image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80',
                'available_sizes': 'S,M,L',
                'available_colors': 'Black,Brown',
                'availability_status': 'in_stock',
            },
            {
                'name': 'Knit Cardigan',
                'description': 'Soft knit cardigan perfect for layering. Features a relaxed fit and subtle pattern.',
                'price': 64.99,
                'category': 'women',
                'image_url': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?ixlib=rb-1.2.1&auto=format&fit=crop&w=668&q=80',
                'available_sizes': 'S,M,L,XL',
                'available_colors': 'Grey,Cream,Pink,Navy',
                'availability_status': 'coming_soon',
            },
        ]

        # Create clothing objects
        products = []
        for item in clothing_data:
            product = Clothing.objects.create(**item)
            products.append(product)
            self.stdout.write(f'Created {item["name"]}')
            
        # Create test users if they don't exist
        usernames = ['user1', 'user2', 'user3', 'user4', 'user5']
        test_users = []
        
        for i, username in enumerate(usernames):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'is_active': True,
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created test user: {username} (password: password123)')
            
            test_users.append(user)
        
        # Add some sample reviews
        self.stdout.write('Adding sample reviews...')
        review_comments = [
            "This is a great product! The quality is excellent and it fits perfectly.",
            "I love this item! The material is soft and comfortable.",
            "Good product for the price. Not perfect but I'm satisfied with my purchase.",
            "Exactly what I was looking for. Would definitely recommend to others.",
            "Very happy with my purchase. Fast shipping and the item is as described.",
            "Nice product, but I expected better quality for the price.",
            "Decent product but sizing runs a bit small. Consider ordering one size up.",
            "The color is slightly different from the pictures, but overall I'm happy with it.",
            "Excellent quality and value for money. Will buy again!",
            "This has become my favorite item in my wardrobe. So versatile!",
        ]
        
        for product in products:
            # Add 2-4 reviews per product with different users
            num_reviews = random.randint(2, 4)
            users_sample = random.sample(test_users, min(num_reviews, len(test_users)))
            
            for i, user in enumerate(users_sample):
                rating = random.randint(3, 5)  # Mostly positive reviews
                comment = random.choice(review_comments)
                
                Review.objects.create(
                    product=product,
                    user=user,
                    rating=rating,
                    comment=comment
                )
                self.stdout.write(f'  Added review for {product.name} by {user.username}')

        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(clothing_data)} clothing items and sample reviews')) 
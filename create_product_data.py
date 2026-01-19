# create_product_data.py
import json
import random
from datetime import datetime, timedelta

categories = ['Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports']
brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
electronics_products = ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Camera']
books_products = ['Fiction Novel', 'Science Book', 'Biography', 'Cookbook', 'Travel Guide']
clothing_products = ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Shoes']
home_products = ['Blender', 'Coffee Maker', 'Vacuum', 'Lamp', 'Bed Sheet']
sports_products = ['Basketball', 'Yoga Mat', 'Dumbbells', 'Tennis Racket', 'Running Shoes']

product_types = {
    'Electronics': electronics_products,
    'Books': books_products,
    'Clothing': clothing_products,
    'Home & Kitchen': home_products,
    'Sports': sports_products
}

def generate_products(n=1000):
    products = []
    
    for i in range(1, n + 1):
        category = random.choice(categories)
        product_type = random.choice(product_types[category])
        brand = random.choice(brands)
        
        # Generate realistic data
        price = round(random.uniform(10, 1000), 2)
        rating = round(random.uniform(2.5, 5.0), 1)
        num_reviews = random.randint(0, 5000)
        view_count = random.randint(100, 50000)
        
        # Sales data
        sales_last_30_days = random.randint(0, 1000)
        
        # Release date (last 3 years)
        days_ago = random.randint(0, 1095)
        release_date = (datetime.now() - timedelta(days=days_ago)).isoformat() + 'Z'
        
        # Discount
        discount = random.choice([0, 5, 10, 15, 20, 25, 30])
        
        product = {
            'id': f'PROD{i:05d}',
            'title': f'{brand} {product_type} - Model {i}',
            'description': f'High quality {product_type.lower()} from {brand}. Perfect for everyday use.',
            'category': category,
            'brand': brand,
            'price': price,
            'rating': rating,
            'num_reviews': num_reviews,
            'view_count': view_count,
            'sales_last_30_days': sales_last_30_days,
            'release_date': release_date,
            'discount_percent': discount,
            'in_stock': random.choice([True, True, True, False]),  # 75% in stock
            'tags': random.sample(['bestseller', 'new', 'trending', 'premium', 'budget-friendly'], 
                                   k=random.randint(0, 3))
        }
        
        products.append(product)
    
    return products

# Generate products
products = generate_products(1000)

# Save as JSON
with open('products.json', 'w') as f:
    json.dump(products, f, indent=2)

print(f"Generated {len(products)} products")
print(f"Sample product: {json.dumps(products[0], indent=2)}")
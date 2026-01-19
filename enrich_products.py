# enrich_products.py
import json
import numpy as np

# Load products
with open('products.json', 'r') as f:
    products = json.load(f)

# Calculate popularity score
for product in products:
    # Weighted popularity formula
    popularity = (
        0.3 * min(product['rating'] / 5.0, 1.0) +
        0.2 * min(product['num_reviews'] / 5000, 1.0) +
        0.3 * min(product['sales_last_30_days'] / 1000, 1.0) +
        0.2 * min(product['view_count'] / 50000, 1.0)
    )
    
    product['popularity_score'] = round(popularity, 4)

# Save enriched data
with open('products_enriched.json', 'w') as f:
    json.dump(products, f, indent=2)

print("Products enriched with popularity scores")
# create_interaction_data.py
import json
import random
from datetime import datetime, timedelta

# Load products
with open('products.json', 'r') as f:
    products = json.load(f)

product_ids = [p['id'] for p in products]

def generate_user_interactions(num_users=500, interactions_per_user=20):
    """Generate realistic user interaction data"""
    interactions = []
    
    for user_id in range(1, num_users + 1):
        # Each user has preferences (categories they like)
        preferred_categories = random.sample(['Electronics', 'Books', 'Clothing', 
                                              'Home & Kitchen', 'Sports'], 
                                            k=random.randint(1, 3))
        
        # Get products in preferred categories
        preferred_products = [p['id'] for p in products 
                             if p['category'] in preferred_categories]
        
        # Generate interactions (80% from preferred, 20% random)
        for _ in range(interactions_per_user):
            if random.random() < 0.8 and preferred_products:
                product_id = random.choice(preferred_products)
            else:
                product_id = random.choice(product_ids)
            
            # Interaction type
            interaction_type = random.choices(
                ['view', 'click', 'add_to_cart', 'purchase'],
                weights=[50, 30, 15, 5]
            )[0]
            
            # Timestamp (last 90 days)
            days_ago = random.randint(0, 90)
            timestamp = (datetime.now() - timedelta(days=days_ago)).isoformat() + 'Z'
            
            interaction = {
                'user_id': f'USER{user_id:05d}',
                'product_id': product_id,
                'interaction_type': interaction_type,
                'timestamp': timestamp,
                'session_id': f'SESSION{random.randint(1, 10000):05d}'
            }
            
            interactions.append(interaction)
    
    return interactions

# Generate interactions
interactions = generate_user_interactions(500, 20)

# Save as JSON
with open('interactions.json', 'w') as f:
    json.dump(interactions, f, indent=2)

print(f"Generated {len(interactions)} interactions")
print(f"Sample interaction: {json.dumps(interactions[0], indent=2)}")
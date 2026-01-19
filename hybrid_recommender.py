# hybrid_recommender.py
import requests
from collaborative_filtering import CollaborativeFilteringRecommender
from content_based_recommender import ContentBasedRecommender
import numpy as np

class HybridRecommender:
    def __init__(self, solr_url="http://localhost:8983/solr/products"):
        self.content_based = ContentBasedRecommender(solr_url)
        self.collaborative = CollaborativeFilteringRecommender()
        self.collaborative.build_matrix().compute_item_similarity()
        self.solr_url = solr_url
    
    def hybrid_recommend(self, product_id, user_id=None, num_recommendations=10, 
                        content_weight=0.5, collab_weight=0.5):
        """
        Hybrid recommendation combining content-based and collaborative filtering
        """
        
        recommendations = {}
        
        # Get content-based recommendations
        content_recs = self.content_based.recommend_similar_products(product_id, 20)
        for rec in content_recs:
            pid = rec['id']
            recommendations[pid] = recommendations.get(pid, 0) + content_weight * rec.get('score', 1.0)
        
        # Get collaborative recommendations
        collab_recs = self.collaborative.recommend_similar_items(product_id, 20)
        for rec in collab_recs:
            pid = rec['product_id']
            recommendations[pid] = recommendations.get(pid, 0) + collab_weight * rec['similarity']
        
        # If user is provided, boost with user-based CF
        if user_id:
            user_recs = self.collaborative.recommend_for_user(user_id, 20)
            for rec in user_recs:
                pid = rec['product_id']
                recommendations[pid] = recommendations.get(pid, 0) + 0.3 * rec['score']
        
        # Sort by combined score
        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        
        # Fetch product details from Solr
        result_products = []
        for pid, score in sorted_recs[:num_recommendations]:
            product = self.content_based.get_product(pid)
            if product:
                product['hybrid_score'] = score
                result_products.append(product)
        
        return result_products
    
    def personalized_recommendations(self, user_id, num_recommendations=10):
        """Generate personalized recommendations for a user"""
        
        # Get user's recent interactions
        user_recs = self.collaborative.recommend_for_user(user_id, num_recommendations)
        
        # Fetch details
        recommendations = []
        for rec in user_recs:
            product = self.content_based.get_product(rec['product_id'])
            if product:
                product['recommendation_score'] = rec['score']
                recommendations.append(product)
        
        return recommendations
    
    def trending_products(self, category=None, num_recommendations=10):
        """Get trending products"""
        
        url = f"{self.solr_url}/select"
        
        params = {
            'q': '*:*',
            'sort': 'sales_last_30_days desc, popularity_score desc',
            'rows': num_recommendations,
            'wt': 'json'
        }
        
        if category:
            params['fq'] = f'category:"{category}"'
        
        response = requests.get(url, params=params)
        return response.json()['response']['docs']

# Test hybrid recommender
if __name__ == '__main__':
    hybrid = HybridRecommender()
    
    product_id = 'PROD00001'
    user_id = 'USER00001'
    
    print(f"\n=== Hybrid Recommendations for Product: {product_id} ===\n")
    recs = hybrid.hybrid_recommend(product_id, user_id, 10)
    
    for i, rec in enumerate(recs, 1):
        print(f"{i}. {rec['title']}")
        print(f"   Category: {rec['category']} | Price: ${rec['price']}")
        print(f"   Hybrid Score: {rec['hybrid_score']:.4f}\n")
    
    print(f"\n=== Personalized Recommendations for User: {user_id} ===\n")
    person_recs = hybrid.personalized_recommendations(user_id, 10)
    
    for i, rec in enumerate(person_recs, 1):
        print(f"{i}. {rec['title']}")
        print(f"   Score: {rec['recommendation_score']:.4f}\n")
    
    print(f"\n=== Trending Products ===\n")
    trending = hybrid.trending_products(num_recommendations=10)
    
    for i, product in enumerate(trending, 1):
        print(f"{i}. {product['title']}")
        print(f"   Sales (30d): {product['sales_last_30_days']} | Popularity: {product['popularity_score']}\n")
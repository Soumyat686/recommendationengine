# content_based_recommender.py
import requests
import json
from collections import defaultdict

SOLR_URL = "http://localhost:8983/solr/products"

class ContentBasedRecommender:
    def __init__(self, solr_url=SOLR_URL):
        self.solr_url = solr_url
    
    def get_product(self, product_id):
        """Get product details"""
        url = f"{self.solr_url}/select"
        params = {
            'q': f'id:{product_id}',
            'wt': 'json'
        }
        response = requests.get(url, params=params)
        docs = response.json()['response']['docs']
        return docs[0] if docs else None
    
    def recommend_similar_products(self, product_id, num_recommendations=10):
        """Recommend products similar to given product"""
        
        # Get source product
        source_product = self.get_product(product_id)
        if not source_product:
            return []
        
        # Build More Like This query
        url = f"{self.solr_url}/select"
        
        params = {
            'q': f'id:{product_id}',
            'mlt': 'true',
            'mlt.fl': 'title,description,category,brand',
            'mlt.mindf': 1,
            'mlt.mintf': 1,
            'rows': num_recommendations,
            'wt': 'json'
        }
        
        response = requests.get(url, params=params)
        result = response.json()
        
        # Get similar products from MLT response
        similar_products = result.get('moreLikeThis', {}).get(product_id, {}).get('docs', [])
        
        return similar_products
    
    def recommend_by_category(self, category, exclude_id=None, num_recommendations=10):
        """Recommend top products in a category"""
        
        url = f"{self.solr_url}/select"
        
        # Build filter query
        fq = f'category:"{category}"'
        if exclude_id:
            fq += f' AND -id:{exclude_id}'
        
        params = {
            'q': '*:*',
            'fq': fq,
            'sort': 'popularity_score desc, rating desc',
            'rows': num_recommendations,
            'wt': 'json'
        }
        
        response = requests.get(url, params=params)
        docs = response.json()['response']['docs']
        
        return docs
    
    def recommend_by_brand(self, brand, exclude_id=None, num_recommendations=10):
        """Recommend products from same brand"""
        
        url = f"{self.solr_url}/select"
        
        fq = f'brand:"{brand}"'
        if exclude_id:
            fq += f' AND -id:{exclude_id}'
        
        params = {
            'q': '*:*',
            'fq': fq,
            'sort': 'popularity_score desc',
            'rows': num_recommendations,
            'wt': 'json'
        }
        
        response = requests.get(url, params=params)
        return response.json()['response']['docs']

# Test the recommender
if __name__ == '__main__':
    recommender = ContentBasedRecommender()
    
    # Get similar products
    product_id = 'PROD00001'
    print(f"\n=== Recommendations for {product_id} ===\n")
    
    product = recommender.get_product(product_id)
    if product:
        print(f"Source Product: {product['title']}")
        print(f"Category: {product['category']}")
        print(f"Brand: {product['brand']}")
        print(f"\nSimilar Products:")
        
        similar = recommender.recommend_similar_products(product_id, 5)
        for i, rec in enumerate(similar, 1):
            print(f"{i}. {rec['title']} (Score: {rec.get('score', 'N/A')})")
        
        print(f"\nTop Products in {product['category']}:")
        category_recs = recommender.recommend_by_category(product['category'], product_id, 5)
        for i, rec in enumerate(category_recs, 1):
            print(f"{i}. {rec['title']} (Popularity: {rec['popularity_score']})")
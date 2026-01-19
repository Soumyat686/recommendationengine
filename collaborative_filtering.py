# collaborative_filtering.py
import json
import numpy as np
from collections import defaultdict
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeFilteringRecommender:
    def __init__(self, interactions_file='interactions.json'):
        self.interactions = self._load_interactions(interactions_file)
        self.user_item_matrix = None
        self.item_similarity = None
        self.user_to_idx = {}
        self.idx_to_user = {}
        self.item_to_idx = {}
        self.idx_to_item = {}
        
    def _load_interactions(self, filename):
        """Load interaction data"""
        with open(filename, 'r') as f:
            return json.load(f)
    
    def build_matrix(self):
        """Build user-item interaction matrix"""
        
        # Create mappings
        users = list(set(i['user_id'] for i in self.interactions))
        items = list(set(i['product_id'] for i in self.interactions))
        
        self.user_to_idx = {u: idx for idx, u in enumerate(users)}
        self.idx_to_user = {idx: u for u, idx in self.user_to_idx.items()}
        self.item_to_idx = {i: idx for idx, i in enumerate(items)}
        self.idx_to_item = {idx: i for i, idx in self.item_to_idx.items()}
        
        # Weight different interaction types
        interaction_weights = {
            'view': 1,
            'click': 2,
            'add_to_cart': 3,
            'purchase': 5
        }
        
        # Build matrix
        rows = []
        cols = []
        data = []
        
        for interaction in self.interactions:
            user_idx = self.user_to_idx[interaction['user_id']]
            item_idx = self.item_to_idx[interaction['product_id']]
            weight = interaction_weights[interaction['interaction_type']]
            
            rows.append(user_idx)
            cols.append(item_idx)
            data.append(weight)
        
        self.user_item_matrix = csr_matrix(
            (data, (rows, cols)),
            shape=(len(users), len(items))
        )
        
        print(f"Built matrix: {len(users)} users × {len(items)} items")
        
        return self
    
    def compute_item_similarity(self):
        """Compute item-item similarity matrix"""
        print("Computing item-item similarity...")
        
        # Transpose to get item-user matrix
        item_user_matrix = self.user_item_matrix.T
        
        # Compute cosine similarity
        self.item_similarity = cosine_similarity(item_user_matrix, dense_output=False)
        
        print("Item similarity computed")
        return self
    
    def recommend_for_user(self, user_id, num_recommendations=10):
        """Recommend items for a user based on their history"""
        
        if user_id not in self.user_to_idx:
            return []
        
        user_idx = self.user_to_idx[user_id]
        
        # Get user's interactions
        user_interactions = self.user_item_matrix[user_idx].toarray().flatten()
        
        # Get items user hasn't interacted with
        interacted_items = set(np.where(user_interactions > 0)[0])
        
        # Compute scores for all items
        scores = self.item_similarity.T.dot(user_interactions)
        
        # Get top recommendations (excluding already interacted)
        recommendations = []
        for item_idx in np.argsort(scores)[::-1]:
            if item_idx not in interacted_items:
                recommendations.append({
                    'product_id': self.idx_to_item[item_idx],
                    'score': scores[item_idx]
                })
            
            if len(recommendations) >= num_recommendations:
                break
        
        return recommendations
    
    def recommend_similar_items(self, product_id, num_recommendations=10):
        """Find similar items based on collaborative filtering"""
        
        if product_id not in self.item_to_idx:
            return []
        
        item_idx = self.item_to_idx[product_id]
        
        # Get similarity scores for this item
        similarity_scores = self.item_similarity[item_idx].toarray().flatten()
        
        # Get top similar items (excluding itself)
        recommendations = []
        for similar_idx in np.argsort(similarity_scores)[::-1][1:]:  # Skip first (itself)
            recommendations.append({
                'product_id': self.idx_to_item[similar_idx],
                'similarity': similarity_scores[similar_idx]
            })
            
            if len(recommendations) >= num_recommendations:
                break
        
        return recommendations

# Test collaborative filtering
if __name__ == '__main__':
    cf_recommender = CollaborativeFilteringRecommender()
    cf_recommender.build_matrix()
    cf_recommender.compute_item_similarity()
    
    # Test user recommendations
    user_id = 'USER00001'
    print(f"\n=== Recommendations for {user_id} ===\n")
    
    user_recs = cf_recommender.recommend_for_user(user_id, 10)
    for i, rec in enumerate(user_recs, 1):
        print(f"{i}. {rec['product_id']} (Score: {rec['score']:.4f})")
    
    # Test item similarity
    product_id = 'PROD00001'
    print(f"\n=== Similar Items to {product_id} ===\n")
    
    item_recs = cf_recommender.recommend_similar_items(product_id, 10)
    for i, rec in enumerate(item_recs, 1):
        print(f"{i}. {rec['product_id']} (Similarity: {rec['similarity']:.4f})")
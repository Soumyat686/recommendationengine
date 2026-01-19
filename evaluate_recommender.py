# evaluate_recommender.py
import json
import numpy as np
from collections import defaultdict
from hybrid_recommender import HybridRecommender

class RecommenderEvaluator:
    def __init__(self, interactions_file='interactions.json'):
        with open(interactions_file, 'r') as f:
            self.interactions = json.load(f)
        
        self.recommender = HybridRecommender()
    
    def split_data(self, test_ratio=0.2):
        """Split interactions into train/test"""
        
        # Group by user
        user_interactions = defaultdict(list)
        for interaction in self.interactions:
            if interaction['interaction_type'] in ['purchase', 'add_to_cart']:
                user_interactions[interaction['user_id']].append(interaction['product_id'])
        
        train_data = {}
        test_data = {}
        
        for user, products in user_interactions.items():
            if len(products) < 2:
                continue
            
            split_point = int(len(products) * (1 - test_ratio))
            train_data[user] = products[:split_point]
            test_data[user] = products[split_point:]
            return train_data, test_data

def precision_at_k(self, recommended, relevant, k=10):
    """Calculate Precision@K"""
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    
    hits = len([r for r in recommended_k if r in relevant_set])
    return hits / k if k > 0 else 0

def recall_at_k(self, recommended, relevant, k=10):
    """Calculate Recall@K"""
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    
    hits = len([r for r in recommended_k if r in relevant_set])
    return hits / len(relevant_set) if len(relevant_set) > 0 else 0

def ndcg_at_k(self, recommended, relevant, k=10):
    """Calculate NDCG@K"""
    recommended_k = recommended[:k]
    relevant_set = set(relevant)
    
    # Binary relevance (1 if relevant, 0 otherwise)
    relevance_scores = [1 if r in relevant_set else 0 for r in recommended_k]
    
    # DCG
    dcg = sum([rel / np.log2(i + 2) for i, rel in enumerate(relevance_scores)])
    
    # IDCG (perfect ranking)
    ideal_scores = sorted(relevance_scores, reverse=True)
    idcg = sum([rel / np.log2(i + 2) for i, rel in enumerate(ideal_scores)])
    
    return dcg / idcg if idcg > 0 else 0

def evaluate(self, k=10):
    """Evaluate recommender system"""
    
    train_data, test_data = self.split_data()
    
    precisions = []
    recalls = []
    ndcgs = []
    
    for user_id, test_products in test_data.items():
        # Get recommendations
        recs = self.recommender.personalized_recommendations(user_id, k)
        recommended_ids = [r['id'] for r in recs]
        
        # Calculate metrics
        p = self.precision_at_k(recommended_ids, test_products, k)
        r = self.recall_at_k(recommended_ids, test_products, k)
        n = self.ndcg_at_k(recommended_ids, test_products, k)
        
        precisions.append(p)
        recalls.append(r)
        ndcgs.append(n)
    
    print(f"\n=== Evaluation Results @ {k} ===")
    print(f"Precision@{k}: {np.mean(precisions):.4f}")
    print(f"Recall@{k}: {np.mean(recalls):.4f}")
    print(f"NDCG@{k}: {np.mean(ndcgs):.4f}")
    print(f"Users evaluated: {len(precisions)}")
    
    return {
        'precision': np.mean(precisions),
        'recall': np.mean(recalls),
        'ndcg': np.mean(ndcgs)
    }

    if name == 'main':
        evaluator = RecommenderEvaluator()
        results = evaluator.evaluate(k=10)
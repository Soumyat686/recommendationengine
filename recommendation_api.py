# recommendation_api.py
from flask import Flask, request, jsonify
from hybrid_recommender import HybridRecommender
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize recommender
recommender = HybridRecommender()

@app.route('/api/recommendations/similar/<product_id>', methods=['GET'])
def get_similar_products(product_id):
    """Get similar products"""
    try:
        num_recs = int(request.args.get('limit', 10))
        user_id = request.args.get('user_id')
        
        recommendations = recommender.hybrid_recommend(
            product_id, 
            user_id=user_id,
            num_recommendations=num_recs
        )
        
        return jsonify({
            'product_id': product_id,
            'recommendations': recommendations,
            'count': len(recommendations)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/user/<user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    """Get personalized recommendations for user"""
    try:
        num_recs = int(request.args.get('limit', 10))
        
        recommendations = recommender.personalized_recommendations(
            user_id,
            num_recommendations=num_recs
        )
        
        return jsonify({
            'user_id': user_id,
            'recommendations': recommendations,
            'count': len(recommendations)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations/trending', methods=['GET'])
def get_trending():
    """Get trending products"""
    try:
        category = request.args.get('category')
        num_recs = int(request.args.get('limit', 10))
        
        trending = recommender.trending_products(
            category=category,
            num_recommendations=num_recs
        )
        
        return jsonify({
            'category': category,
            'trending': trending,
            'count': len(trending)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'recommendation-engine'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Blueprint, request, jsonify
from models import db, Review_travel
from datetime import datetime
# Define Blueprint
travel_review_bp = Blueprint("travel_review_bp", __name__)

@travel_review_bp.route('/reviews', methods=['POST'])
def create_review():
    data = request.json
    if not data or not all(key in data for key in ('rating', 'review', 'user_id', 'travel_id')):
        return jsonify({"error": "Invalid data. Make sure to include rating, review, user_id, and travel_id."}), 400

    try:
        new_review = Review_travel(
            rating=data['rating'],
            review=data['review'],
            user_id=data['user_id'],
            travel_id=data['travel_id']
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review created", "review_id": new_review.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create review. {str(e)}"}), 500
    finally:
        db.session.close()

@travel_review_bp.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review_travel.query.all()
    serialized_reviews = []
    for review in reviews:
        serialized_review = {
            'id': review.id,
            'rating': review.rating,
            'review': review.review,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat(),
            'user_id': review.user_id,
            'travel_id': review.travel_id,
            'review_count': review.review_count
        }
        serialized_reviews.append(serialized_review)
    return jsonify(serialized_reviews)


@travel_review_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review_travel.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    return jsonify({
        'id': review.id,
        'rating': review.rating,
        'review': review.review,
        'created_at': review.created_at.isoformat(),
        'updated_at': review.updated_at.isoformat(),
        'user_id': review.user_id,
        'travel_id': review.travel_id,
        'review_count': review.review_count
    })



@travel_review_bp.route('/reviews/<int:review_id>', methods=['PATCH'])
def update_review(review_id):
    review = Review_travel.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    data = request.json
    for key, value in data.items():
        # Convert string representations to datetime objects if applicable
        if key in ['created_at', 'updated_at']:
            value = datetime.fromisoformat(value)
        setattr(review, key, value)

    db.session.commit()

    return jsonify({"message": "Review updated", "review": {
        'id': review.id,
        'rating': review.rating,
        'review': review.review,
        'created_at': review.created_at.isoformat(),
        'updated_at': review.updated_at.isoformat(),
        'user_id': review.user_id,
        'travel_id': review.travel_id,
        'review_count': review.review_count
    }})


@travel_review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review_travel.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Review deleted"})

from flask import Blueprint, jsonify, request, abort
from models import db, Review_accomodation
from flask_jwt_extended import jwt_required


accomodation_review_bp = Blueprint('accomodation_review_bp', __name__)



@accomodation_review_bp.route('/accomodation-reviews', methods=['POST'])
@jwt_required()

def create_review():
    # Check if the request Content-Type is 'application/json'
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({"error": "Unsupported Media Type. Content-Type must be 'application/json'."}), 415

    data = request.json
    if not data or not all(key in data for key in ('rating', 'review', 'user_id', 'accomodation_id')):
        return jsonify({"error": "Invalid data. Make sure to include rating, review, user_id, and accomodation_id."}), 400

    try:
        new_review = Review_accomodation(
            rating=data['rating'],
            review=data['review'],
            user_id=data['user_id'],
            accomodation_id=data['accomodation_id']
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review created", "review_id": new_review.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to create review. {str(e)}"}), 500
    finally:
        db.session.close()


@accomodation_review_bp.route('/accomodation-reviews', methods=['GET'])
@jwt_required()

def get_reviews():
    reviews = Review_accomodation.query.all()
    serialized_reviews = []
    for review in reviews:
        serialized_review = {
            'id': review.id,
            'rating': review.rating,
            'review': review.review,
            'created_at': review.created_at.isoformat() if review.created_at else None,
            'updated_at': review.updated_at.isoformat() if review.updated_at else None,
            'user_id': review.user_id,
            'accomodation_id': review.accomodation_id,
            'review_count': review.review_count
        }
        serialized_reviews.append(serialized_review)
    return jsonify(serialized_reviews)




@accomodation_review_bp.route('/accomodation-reviews/<int:review_id>', methods=['GET'])
@jwt_required()

def get_review(review_id):
    review = Review_accomodation.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    
    serialized_review = {
        'id': review.id,
        'rating': review.rating,
        'review': review.review,
        'created_at': review.created_at.isoformat() if review.created_at else None,
        'updated_at': review.updated_at.isoformat() if review.updated_at else None,
        'user_id': review.user_id,
        'accomodation_id': review.accomodation_id,
        'review_count': review.review_count
    }
    return jsonify(serialized_review)


@accomodation_review_bp.route('/accomodation-reviews/<int:review_id>', methods=['PATCH'])
@jwt_required()

def update_review(review_id):
    review = Review_accomodation.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    data = request.json
    for key, value in data.items():
        # Check if the value is a string before attempting to parse it
        if isinstance(value, str):
            try:
                setattr(review, key, value)
            except ValueError:
                return jsonify({"error": "Invalid datetime format"}), 400
        else:
            setattr(review, key, value)

    db.session.commit()

    return jsonify({"message": "Review updated", "review": {
        'id': review.id,
        'rating': review.rating,
        'review': review.review,
        'created_at': review.created_at.isoformat(),
        'updated_at': review.updated_at.isoformat(),
        'user_id': review.user_id,
        'accomodation_id': review.accomodation_id,
        'review_count': review.review_count
    }})
@accomodation_review_bp.route('/accomodation-reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()

def delete_review(review_id):
    review = Review_accomodation.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({"message": "Review deleted"})
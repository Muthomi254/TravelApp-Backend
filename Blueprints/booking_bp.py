from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Travel_booking, Accomodation_booking, Reservation_travel, Reservation_accomodation

booking_bp = Blueprint('booking_bp', __name__)


#travel booking
@booking_bp.route('/bookings/travel', methods=['POST'])
@jwt_required()
def book_travel():
    try:
        current_user_id = get_jwt_identity()
        data = request.json
        new_booking = Travel_booking(
            travelling_reservation_id=data['travelling_reservation_id'],
            travelling_service_id=data['travelling_service_id'],
            user_id=current_user_id  # Associate the booking with the current user
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({'message': 'Travel booking created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@booking_bp.route('/bookings/accommodation', methods=['POST'])
@jwt_required()
def book_accommodation():
    try:
        current_user_id = get_jwt_identity()
        data = request.json
        new_booking = Accomodation_booking(
            accomodation_reservation_id=data['accomodation_reservation_id'],
            accomodation_service_id=data['accomodation_service_id'],
            user_id=current_user_id  # Associate the booking with the current user
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({'message': 'Accommodation booking created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@booking_bp.route('/bookings/travel/<int:id>', methods=['PATCH'])
@jwt_required()
def update_travel_booking(id):
    try:
        data = request.json
        booking = Travel_booking.query.get_or_404(id)
        # Add authorization check here if necessary
        booking.travelling_reservation_id = data['travelling_reservation_id']
        booking.travelling_service_id = data['travelling_service_id']
        db.session.commit()
        return jsonify({'message': 'Travel booking updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@booking_bp.route('/bookings/travel/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_travel_bookings(user_id):
    try:
        travel_bookings = Travel_booking.query.filter_by(user_id=user_id).all()
        serialized_bookings = []
        for booking in travel_bookings:
            serialized_booking = {
                'id': booking.id,
                'travelling_reservation_id': booking.travelling_reservation_id,
                'travelling_service_id': booking.travelling_service_id,
                # Add other attributes as needed
            }
            serialized_bookings.append(serialized_booking)
        return jsonify(serialized_bookings), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500        

@booking_bp.route('/bookings/travel/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_travel_booking(id):
    try:
        booking = Travel_booking.query.get_or_404(id)
        # Add authorization check here if necessary
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Travel booking deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Accommodation booking
@booking_bp.route('/bookings/accommodation/<int:id>', methods=['PATCH'])
@jwt_required()
def update_accommodation_booking(id):
    try:
        data = request.json
        booking = Accommodation_booking.query.get_or_404(id)
        # Add authorization check here if necessary
        booking.accommodation_reservation_id = data['accommodation_reservation_id']
        booking.accommodation_service_id = data['accommodation_service_id']
        db.session.commit()
        return jsonify({'message': 'Accommodation booking updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@booking_bp.route('/bookings/accommodation/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_accommodation_bookings(user_id):
    try:
        accomodation_bookings = Accomodation_booking.query.filter_by(user_id=user_id).all()
        serialized_bookings = []
        for booking in accomodation_bookings:
            serialized_booking = {
                'id': booking.id,
                'accomodation_reservation_id': booking.accomodation_reservation_id,
                'accomodation_service_id': booking.accomodation_service_id,
                # Add other attributes as needed
            }
            serialized_bookings.append(serialized_booking)
        return jsonify(serialized_bookings), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        

@booking_bp.route('/bookings/accommodation/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_accommodation_booking(id):
    try:
        booking = Accommodation_booking.query.get_or_404(id)
        # Add authorization check here if necessary
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Accommodation booking deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/total-price', methods=['GET'])
@jwt_required()
def get_total_price():
    try:
        # Fetch all travel bookings
        travel_bookings = Travel_booking.query.all()
        # Calculate total price for all travel bookings
        total_travel_price = sum(booking.travelling_service.price for booking in travel_bookings)

        # Fetch all accommodation bookings
        accomodation_bookings = Accomodation_booking.query.all()
        # Calculate total price for all accommodation bookings
        total_accomodation_price = sum(booking.accomodation_service.price_per_night for booking in accomodation_bookings)

        # Calculate total price for all bookings
        total_price = total_travel_price + total_accomodation_price
        
        return jsonify({'total_price': total_price}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

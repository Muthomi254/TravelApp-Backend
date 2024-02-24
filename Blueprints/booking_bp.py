from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models import db, travel_booking, Accomodation_booking

booking_bp = Blueprint('booking_bp', __name__)

@booking_bp.route('/bookings/travel', methods=['POST'])
@jwt_required()
def book_travel():
    try:
        data = request.json
        new_booking = travel_booking(
            travelling_reservation_id=data['travelling_reservation_id'],
            travelling_service_id=data['travelling_service_id']
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
        data = request.json
        new_booking = Accomodation_booking(
            accomodation_reservation_id=data['accomodation_reservation_id'],
            accomodation_service_id=data['accomodation_service_id']
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
        booking = travel_booking.query.get_or_404(id)
        # Add authorization check here if necessary
        booking.travelling_reservation_id = data['travelling_reservation_id']
        booking.travelling_service_id = data['travelling_service_id']
        db.session.commit()
        return jsonify({'message': 'Travel booking updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/travel/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_travel_booking(id):
    try:
        booking = travel_booking.query.get_or_404(id)
        # Add authorization check here if necessary
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Travel booking deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/accommodation/<int:id>', methods=['PATCH'])
@jwt_required()
def update_accommodation_booking(id):
    try:
        data = request.json
        booking = Accomodation_booking.query.get_or_404(id)
        # Add authorization check here if necessary
        booking.accomodation_reservation_id = data['accomodation_reservation_id']
        booking.accomodation_service_id = data['accomodation_service_id']
        db.session.commit()
        return jsonify({'message': 'Accommodation booking updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booking_bp.route('/bookings/accommodation/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_accommodation_booking(id):
    try:
        booking = Accomodation_booking.query.get_or_404(id)
        # Add authorization check here if necessary
        db.session.delete(booking)
        db.session.commit()
        return jsonify({'message': 'Accommodation booking deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

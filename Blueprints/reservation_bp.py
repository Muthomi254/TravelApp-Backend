from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Reservation_accomodation, Reservation_travel

reservation_bp = Blueprint('reservation_bp', __name__)

@reservation_bp.route('/reservations/accommodation', methods=['POST'])
@jwt_required()
def create_accommodation_reservation():
    try:
        data = request.json
        new_reservation = Reservation_accomodation(
            people_included=data['people_included'],
            user_id=get_jwt_identity()  # Assuming you are using JWT for user authentication
        )
        db.session.add(new_reservation)
        db.session.commit()
        return jsonify({'message': 'Accommodation reservation created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reservation_bp.route('/reservations/travel', methods=['POST'])
@jwt_required()
def create_travel_reservation():
    try:
        data = request.json
        new_reservation = Reservation_travel(
            people_included=data['people_included'],
            checkin=data['checkin'],
            checkout=data['checkout'],
            days_in_room=data['days_in_room'],
            rooms=data['rooms'],
            user_id=get_jwt_identity()  # Assuming you are using JWT for user authentication
        )
        db.session.add(new_reservation)
        db.session.commit()
        return jsonify({'message': 'Travel reservation created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reservation_bp.route('/reservations/accommodation/<int:id>', methods=['GET'])
@jwt_required()
def get_accommodation_reservation(id):
    try:
        reservation = Reservation_accomodation.query.get_or_404(id)
        if reservation.user_id == get_jwt_identity():
            return jsonify({
                'id': reservation.id,
                'people_included': reservation.people_included,
                'date': reservation.date
            }), 200
        else:
            return jsonify({'error': 'Unauthorized access to reservation'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reservation_bp.route('/reservations/travel/<int:id>', methods=['GET'])
@jwt_required()
def get_travel_reservation(id):
    try:
        reservation = Reservation_travel.query.get_or_404(id)
        if reservation.user_id == get_jwt_identity():
            return jsonify({
                'id': reservation.id,
                'people_included': reservation.people_included,
                'date': reservation.date,
                'checkin': reservation.checkin,
                'checkout': reservation.checkout,
                'days_in_room': reservation.days_in_room,
                'rooms': reservation.rooms
            }), 200
        else:
            return jsonify({'error': 'Unauthorized access to reservation'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reservation_bp.route('/reservations/accommodation/<int:id>', methods=['PATCH'])
@jwt_required()
def update_accommodation_reservation(id):
    try:
        data = request.json
        reservation = Reservation_accomodation.query.get_or_404(id)
        if reservation.user_id != get_jwt_identity():
            return jsonify({'error': 'Unauthorized access to reservation'}), 403
        reservation.people_included = data.get('people_included', reservation.people_included)
        db.session.commit()
        return jsonify({'message': 'Accommodation reservation updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reservation_bp.route('/reservations/travel/<int:id>', methods=['PATCH'])
@jwt_required()
def update_travel_reservation(id):
    try:
        data = request.json
        reservation = Reservation_travel.query.get_or_404(id)
        if reservation.user_id != get_jwt_identity():
            return jsonify({'error': 'Unauthorized access to reservation'}), 403
        reservation.people_included = data.get('people_included', reservation.people_included)
        reservation.checkin = data.get('checkin', reservation.checkin)
        reservation.checkout = data.get('checkout', reservation.checkout)
        reservation.days_in_room = data.get('days_in_room', reservation.days_in_room)
        reservation.rooms = data.get('rooms', reservation.rooms)
        db.session.commit()
        return jsonify({'message': 'Travel reservation updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reservation_bp.route('/reservations/accommodation/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_accommodation_reservation(id):
    try:
        reservation = Reservation_accomodation.query.get_or_404(id)
        if reservation.user_id == get_jwt_identity():
            db.session.delete(reservation)
            db.session.commit()
            return jsonify({'message': 'Accommodation reservation deleted successfully'}), 200
        else:
            return jsonify({'error': 'Unauthorized access to reservation'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reservation_bp.route('/reservations/travel/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_travel_reservation(id):
    try:
        reservation = Reservation_travel.query.get_or_404(id)
        if reservation.user_id == get_jwt_identity():
            db.session.delete(reservation)
            db.session.commit()
            return jsonify({'message': 'Travel reservation deleted successfully'}), 200
        else:
            return jsonify({'error': 'Unauthorized access to reservation'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500



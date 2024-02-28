from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Reservation_travel, Travelling_service, Reservation_accomodation, Accomodation_service
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

reservation_bp = Blueprint('reservation_bp', __name__)

# Travel Reservations Routes

@reservation_bp.route('/reservations/travel', methods=['GET'])
def get_all_travel_reservations():
    try:
        user_id = get_jwt_identity()
        reservations = Reservation_travel.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': reservation.id,
            'people_included': reservation.people_included,
            'date': reservation.date,
            'total_price': reservation.price_net,
            # Add other fields as needed
        } for reservation in reservations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reservation_bp.route('/reservations/travel/<int:id>', methods=['GET'])
def get_travel_reservation(id):
    try:
        reservation = Reservation_travel.query.filter_by(id=id).one()
        return jsonify({
            'id': reservation.id,
            'people_included': reservation.people_included,
            'date': reservation.date,
            'total_price': reservation.price_net,
            # Add other fields as needed
        }), 200
    except NoResultFound:
        return jsonify({'error': 'Reservation not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reservation_bp.route('/reservations/travel', methods=['POST'])
@jwt_required()
def create_travel_reservation():
    try:
        data = request.get_json()
        people_included = data.get('people_included')
        service_id = data.get('service_id')  # Use get method to safely retrieve data
        
        if people_included is None or service_id is None:
            return jsonify({'error': 'Missing required data: people_included or service_id'}), 400
        
        # Fetch the traveling service based on the provided service_id
        service = Travelling_service.query.get(service_id)
        if not service:
            return jsonify({'error': 'Traveling service not found'}), 404
        
        # Calculate total net price based on the service's price
        total_price = service.price * people_included
        
        new_reservation = Reservation_travel(
            people_included=people_included,
            price_net=total_price,
            service_id=service_id,  # Assign the service_id to the reservation
            user_id=get_jwt_identity()
        )
        db.session.add(new_reservation)
        db.session.commit()
        return jsonify({'message': 'Travel reservation created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reservation_bp.route('/reservations/travel/<int:id>', methods=['PATCH'])
@jwt_required()
def update_travel_reservation(id):
    try:
        data = request.get_json()
        reservation = Reservation_travel.query.get(id)
        if not reservation:
            raise NoResultFound("Reservation not found")
        if reservation.user_id != get_jwt_identity():
            return jsonify({'error': 'Unauthorized access to reservation'}), 403
        
        # Fetch the traveling service based on the provided service_id
        service_id = reservation.service_id  # Assuming service_id is stored in the reservation object
        service = Travelling_service.query.get(service_id)
        if not service:
            return jsonify({'error': 'Traveling service not found'}), 404
        
        # Calculate total net price based on the service's price and updated number of people included
        reservation.people_included = data.get('people_included', reservation.people_included)
        total_price = service.price * reservation.people_included
        
        # Update the reservation with the new total price
        reservation.price_net = total_price
        
        # Update the reservation date if provided in the request
        if 'datetime' in data:
            reservation.datetime = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S')
        
        # If neither people_included nor datetime is provided, return an error
        if 'people_included' not in data and 'datetime' not in data:
            return jsonify({'error': 'No fields to update provided'}), 400
        
        
        db.session.commit()
        return jsonify({'message': 'Travel reservation updated successfully'}), 200
    except NoResultFound:
        return jsonify({'error': 'Reservation not found'}), 404
    except ValueError:
        return jsonify({'error': 'Invalid date format. Date should be in YYYY-MM-DD format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reservation_bp.route('/reservations/travel/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_travel_reservation(id):
    try:
        reservation = Reservation_travel.query.get(id)
        if not reservation:
            raise NoResultFound("Reservation not found")
        if reservation.user_id != get_jwt_identity():
            return jsonify({'error': 'Unauthorized access to reservation'}), 403
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({'message': 'Travel reservation deleted successfully'}), 200
    except NoResultFound:
        return jsonify({'error': 'Reservation not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Accommodation Reservations Routes
@reservation_bp.route('/reservations/accommodation', methods=['GET'])
@jwt_required()
def get_all_accommodation_reservations():
    try:
        reservations = Reservation_accomodation.query.all()
        return jsonify([{
            'id': reservation.id,
            'people_included': reservation.people_included,
            'date': reservation.date,
            # Add other fields as needed
        } for reservation in reservations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reservation_bp.route('/reservations/accommodation/<int:id>', methods=['GET'])
@jwt_required()
def get_accommodation_reservation(id):
    try:
        user_id = get_jwt_identity()
        reservation = Reservation_accomodation.query.filter_by(id=id, user_id=user_id).one()
        return jsonify({
            'id': reservation.id,
            'people_included': reservation.people_included,
            'date': reservation.date,
            # Add other fields as needed
        }), 200
    except NoResultFound:
        return jsonify({'error': 'Reservation not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reservation_bp.route('/reservations/accommodation', methods=['POST'])
@jwt_required()
def create_accommodation_reservation():
    try:
        data = request.get_json()
        checkin_date = datetime.strptime(data['checkin'], '%Y-%m-%d').date()
        checkout_date = datetime.strptime(data['checkout'], '%Y-%m-%d').date()
        
        # Calculate the number of days in the room
        days_in_room = data['days_in_room']
        
        # Fetch the accommodation service based on the provided service_id
        service_id = data['service_id']
        service = Accomodation_service.query.get(service_id)
        if not service:
            return jsonify({'error': 'Accommodation service not found'}), 404
        
        # Calculate total net price based on the service's price_per_night, rooms, and days_in_room
        total_price = service.price_per_night * data['rooms'] * days_in_room
        
        new_reservation = Reservation_accomodation(
            people_included=data['people_included'],
            checkin=checkin_date,
            checkout=checkout_date,
            days_in_room=days_in_room,
            rooms=data['rooms'],
            service_id=service_id,
            user_id=get_jwt_identity(),
            price_net=total_price
        )
        db.session.add(new_reservation)
        db.session.commit()
        return jsonify({'message': 'Accommodation reservation created successfully'}), 201
    except KeyError as e:
        return jsonify({'error': f'Missing key in request data: {e}'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid date format. Date should be in YYYY-MM-DD format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500






@reservation_bp.route('/reservations/accommodation/<int:id>', methods=['PATCH'])
@jwt_required()
def update_accommodation_reservation(id):
    try:
        data = request.get_json()
        reservation = Reservation_accomodation.query.get(id)
        if not reservation:
            raise NoResultFound("Reservation not found")
        if reservation.user_id != get_jwt_identity():
            return jsonify({'error': 'Unauthorized access to reservation'}), 403
        
        # Update the reservation with the new number of rooms and days in room
        reservation.rooms = data.get('rooms', reservation.rooms)
        reservation.days_in_room = data.get('days_in_room', reservation.days_in_room)
        
        # Fetch the accommodation service based on the reservation's service_id
        service = Accomodation_service.query.get(reservation.service_id)
        if not service:
            return jsonify({'error': 'Accommodation service not found'}), 404
        
        # Calculate total net price based on the updated number of rooms and days in room
        total_price = reservation.rooms * reservation.days_in_room * service.price_per_night
        
        # Update the reservation with the new total price
        reservation.price_net = total_price
        
        # If neither rooms nor days_in_room is provided, return an error
        if 'rooms' not in data and 'days_in_room' not in data:
            return jsonify({'error': 'No fields to update provided'}), 400
        
        db.session.commit()
        return jsonify({'message': 'Accommodation reservation updated successfully'}), 200
    except NoResultFound:
        return jsonify({'error': 'Reservation not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500





@reservation_bp.route('/reservations/accommodation/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_accommodation_reservation(id):
    try:
        reservation = Reservation_accomodation.query.get(id)
        if not reservation:
            raise NoResultFound("Reservation not found")
        if reservation.user_id != get_jwt_identity():
            return jsonify({'error': 'Unauthorized access to reservation'}), 403
        db.session.delete(reservation)
        db.session.commit()
        return jsonify({'message': 'Accommodation reservation deleted successfully'}), 200
    except NoResultFound:
        return jsonify({'error': 'Reservation not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500



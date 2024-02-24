# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from models import db, Reservation_travel, Reservation_accomodation
# from datetime import datetime
# from sqlalchemy.orm.exc import NoResultFound

# reservation_bp = Blueprint('reservation_bp', __name__)

# # Travel Reservations Routes
# @reservation_bp.route('/reservations/travel', methods=['GET'])
# @jwt_required()
# def get_all_travel_reservations():
#     try:
#         user_id = get_jwt_identity()
#         reservations = Reservation_travel.query.filter_by(user_id=user_id).all()
#         return jsonify([{
#             'id': reservation.id,
#             'people_included': reservation.people_included,
#             'date': reservation.date,
#             # Add other fields as needed
#         } for reservation in reservations]), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @reservation_bp.route('/reservations/travel/<int:id>', methods=['GET'])
# @jwt_required()
# def get_travel_reservation(id):
#     try:
#         user_id = get_jwt_identity()
#         reservation = Reservation_travel.query.filter_by(id=id, user_id=user_id).one()
#         return jsonify({
#             'id': reservation.id,
#             'people_included': reservation.people_included,
#             'date': reservation.date,
#             # Add other fields as needed
#         }), 200
#     except NoResultFound:
#         return jsonify({'error': 'Reservation not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @reservation_bp.route('/reservations/travel', methods=['POST'])
# @jwt_required()
# def create_travel_reservation():
#     try:
#         data = request.json
#         new_reservation = Reservation_travel(
#             people_included=data['people_included'],
#             user_id=get_jwt_identity()
#         )
#         db.session.add(new_reservation)
#         db.session.commit()
#         return jsonify({'message': 'Travel reservation created successfully'}), 201
#     except KeyError as e:
#         return jsonify({'error': f'Missing key in request data: {e}'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @reservation_bp.route('/reservations/travel/<int:id>', methods=['PATCH'])
# @jwt_required()
# def update_travel_reservation(id):
#     try:
#         data = request.json
#         reservation = Reservation_travel.query.get(id)
#         if not reservation:
#             raise NoResultFound("Reservation not found")
#         if reservation.user_id != get_jwt_identity():
#             return jsonify({'error': 'Unauthorized access to reservation'}), 403
#         reservation.people_included = data.get('people_included', reservation.people_included)
#         db.session.commit()
#         return jsonify({'message': 'Travel reservation updated successfully'}), 200
#     except NoResultFound:
#         return jsonify({'error': 'Reservation not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @reservation_bp.route('/reservations/travel/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_travel_reservation(id):
#     try:
#         reservation = Reservation_travel.query.get(id)
#         if not reservation:
#             raise NoResultFound("Reservation not found")
#         if reservation.user_id != get_jwt_identity():
#             return jsonify({'error': 'Unauthorized access to reservation'}), 403
#         db.session.delete(reservation)
#         db.session.commit()
#         return jsonify({'message': 'Travel reservation deleted successfully'}), 200
#     except NoResultFound:
#         return jsonify({'error': 'Reservation not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Accommodation Reservations Routes
# @reservation_bp.route('/reservations/accommodation', methods=['GET'])
# @jwt_required()
# def get_all_accommodation_reservations():
#     try:
#         user_id = get_jwt_identity()
#         reservations = Reservation_accomodation.query.filter_by(user_id=user_id).all()
#         return jsonify([{
#             'id': reservation.id,
#             'people_included': reservation.people_included,
#             'date': reservation.date,
#             # Add other fields as needed
#         } for reservation in reservations]), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @reservation_bp.route('/reservations/accommodation/<int:id>', methods=['GET'])
# @jwt_required()
# def get_accommodation_reservation(id):
#     try:
#         user_id = get_jwt_identity()
#         reservation = Reservation_accomodation.query.filter_by(id=id, user_id=user_id).one()
#         return jsonify({
#             'id': reservation.id,
#             'people_included': reservation.people_included,
#             'date': reservation.date,
#             # Add other fields as needed
#         }), 200
#     except NoResultFound:
#         return jsonify({'error': 'Reservation not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @reservation_bp.route('/reservations/accommodation', methods=['POST'])
# @jwt_required()
# def create_accommodation_reservation():
#     try:
#         data = request.json
#         checkin_date = datetime.strptime(data['checkin'], '%Y-%m-%d').date()
#         checkout_date = datetime.strptime(data['checkout'], '%Y-%m-%d').date()
#         new_reservation = Reservation_accomodation(
#             people_included=data['people_included'],
#             checkin=checkin_date,
#             checkout=checkout_date,
#             days_in_room=data['days_in_room'],
#             rooms=data['rooms'],
#             user_id=get_jwt_identity(),
#             price_net=data['price_net']
#         )
#         db.session.add(new_reservation)
#         db.session.commit()
#         return jsonify({'message': 'Accommodation reservation created successfully'}), 201
#     except KeyError as e:
#         return jsonify({'error': f'Missing key in request data: {e}'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @reservation_bp.route('/reservations/accommodation/<int:id>', methods=['PATCH'])
# @jwt_required()
# def update_accommodation_reservation(id):
#     try:
#         data = request.json
#         reservation = Reservation_accomodation.query.get(id)
#         if not reservation:
#             raise NoResultFound("Reservation not found")
#         if reservation.user_id != get_jwt_identity():
#             return jsonify({'error': 'Unauthorized access to reservation'}), 403
#         reservation.people_included = data.get('people_included', reservation.people_included)
#         db.session.commit()
#         return jsonify({'message': 'Accommodation reservation updated successfully'}), 200
#     except NoResultFound:
#         return jsonify({'error': 'Reservation not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @reservation_bp.route('/reservations/accommodation/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_accommodation_reservation(id):
#     try:
#         reservation = Reservation_accomodation.query.get(id)
#         if not reservation:
#             raise NoResultFound("Reservation not found")
#         if reservation.user_id != get_jwt_identity():
#             return jsonify({'error': 'Unauthorized access to reservation'}), 403
#         db.session.delete(reservation)
#         db.session.commit()
#         return jsonify({'message': 'Accommodation reservation deleted successfully'}), 200
#     except NoResultFound:
#         return jsonify({'error': 'Reservation not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500



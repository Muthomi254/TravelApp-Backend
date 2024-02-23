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

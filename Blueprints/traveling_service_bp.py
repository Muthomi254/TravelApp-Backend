
from flask import Blueprint, jsonify, request, abort
from models import db, Travelling_service
from flask_jwt_extended import jwt_required
from datetime import datetime

# Create a Blueprint for service routes
traveling_service_bp = Blueprint('traveling_service_bp', __name__)

# Route to get all travel services
@traveling_service_bp.route('/travel', methods=['GET'])
# @jwt_required()
def get_travel_services():
    try:
        travel_services = Travelling_service.query.all()
        serialized_services = []
        for service in travel_services:
            serialized_service = {
                "id": service.id,
                "name": service.name,
                "seats": service.seats,
                "departure_time": service.departure_time.strftime('%Y-%m-%d %H:%M:%S'),
                "arrival_time": service.arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
                "description": service.description,
                "price": service.price,
                "departure_city": service.departure_city,
                "arrival_city": service.arrival_city,
                "registration_number": service.registration_number,
                "company_id": service.company_id,
                "image": service.image,  # Include image in serialized service
                "vehicle_type": service.vehicle_type
            }
            serialized_services.append(serialized_service)
        return jsonify({"success": True, "data": serialized_services}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get a single travel service by ID
@traveling_service_bp.route('/travel/<int:service_id>', methods=['GET'])
# @jwt_required()
def get_travel_service(service_id):
    try:
        service = Travelling_service.query.get_or_404(service_id)
        serialized_service = {
            "id": service.id,
            "name": service.name,
            "seats": service.seats,
            "departure_time": service.departure_time.strftime('%Y-%m-%d %H:%M:%S'),
            "arrival_time": service.arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
            "description": service.description,
            "price": service.price,
            "departure_city": service.departure_city,
            "arrival_city": service.arrival_city,
            "registration_number": service.registration_number,
            "company_id": service.company_id,
            "image": service.image,  # Include image in serialized service
            "vehicle_type": service.vehicle_type
        }
        return jsonify({"success": True, "data": serialized_service}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to create a new travel service


@traveling_service_bp.route('/travel', methods=['POST'])
def create_travel_service():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Convert string representations of time to datetime objects
        data['departure_time'] = datetime.strptime(data['departure_time'], '%Y-%m-%dT%H:%M:%S')
        data['arrival_time'] = datetime.strptime(data['arrival_time'], '%Y-%m-%dT%H:%M:%S')

        new_service = Travelling_service(**data)
        db.session.add(new_service)
        db.session.commit()
        
        return jsonify(new_service.to_dict()), 201
    except ValueError:
        return jsonify({"error": "Invalid data format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to update an existing travel service
@traveling_service_bp.route('/travel/<int:service_id>', methods=['PUT', 'PATCH'])
# @jwt_required()
def update_travel_service(service_id):
    try:
        service = Travelling_service.query.get_or_404(service_id)
        data = request.json
        # Convert 'departure_time' and 'arrival_time' strings to datetime objects
        departure_time = datetime.strptime(data['departure_time'], '%Y-%m-%dT%H:%M:%S')
        arrival_time = datetime.strptime(data['arrival_time'], '%Y-%m-%dT%H:%M:%S')
        # Update the service object with the new values
        service.name = data.get('name', service.name)
        service.departure_time = departure_time
        service.arrival_time = arrival_time
        service.price = data.get('price', service.price)
        service.seats = data.get('seats', service.seats)
        service.description = data.get('description', service.description)
        service.departure_city = data.get('departure_city', service.departure_city)
        service.arrival_city = data.get('arrival_city', service.arrival_city)
        service.image = data.get('image', service.image)  # Update image if provided
        service.vehicle_type = data.get('vehicle_type', service.vehicle_type)  # Update vehicle_type if provided
        # Commit the changes to the database
        db.session.commit()
        # Serialize the updated service object
        serialized_service = {
            "id": service.id,
            "name": service.name,
            "seats": service.seats,
            "departure_time": service.departure_time.strftime('%Y-%m-%d %H:%M:%S'),
            "arrival_time": service.arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
            "description": service.description,
            "price": service.price,
            "departure_city": service.departure_city,
            "arrival_city": service.arrival_city,
            "registration_number": service.registration_number,
            "company_id": service.company_id,
            "image": service.image,  # Include image in serialized service
            "vehicle_type": service.vehicle_type  # Include vehicle_type in serialized service
        }
        # Return the serialized service as JSON response
        return jsonify({"success": True, "message": "Travel service updated successfully", "data": serialized_service}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to delete an existing travel service
@traveling_service_bp.route('/travel/<int:service_id>', methods=['DELETE'])
# @jwt_required()
def delete_travel_service(service_id):
    try:
        service = Travelling_service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return jsonify({"success": True, "message": "Travel service deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import Blueprint, jsonify, request
from models import db, Travelling_service
from datetime import datetime

# Create a Blueprint for service routes

traveling_service_bp = Blueprint('traveling_service_bp', __name__)

# Route to get all travel services

@traveling_service_bp.route('/travel', methods=['GET'])
def get_travel_services():
    travel_services = Travelling_service.query.all()
    
    # Manually serialize each object
    serialized_services = []
    for service in travel_services:
        serialized_service = {
            "id": service.id,
            "name": service.name,
            "seats": service.seats,
            "depurture_time": service.depurture_time.strftime('%Y-%m-%d %H:%M:%S'),
            "arrival_time": service.arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
            "description": service.description,
            "price": service.price,
            "depurture_city": service.depurture_city,
            "arrival_city": service.arrival_city,
            "registration_number": service.registration_number,
            "company_id": service.company_id
        }
        serialized_services.append(serialized_service)
    
    return jsonify(serialized_services)

@traveling_service_bp.route('/travel/<int:service_id>', methods=['GET'])
def get_travel_service(service_id):
    service = Travelling_service.query.get_or_404(service_id)
    serialized_service = {
        "id": service.id,
        "name": service.name,
        "seats": service.seats,
        "depurture_time": service.depurture_time.strftime('%Y-%m-%d %H:%M:%S'),
        "arrival_time": service.arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
        "description": service.description,
        "price": service.price,
        "depurture_city": service.depurture_city,
        "arrival_city": service.arrival_city,
        "registration_number": service.registration_number,
        "company_id": service.company_id
    }
    return jsonify(serialized_service) 

  


# Route to create a new travel service
@traveling_service_bp.route('/travel', methods=['POST'])
def create_travel_service():
    try:
        data = request.json
        print("Received JSON data:", data)
        
        # Remove the 'id' field from the data as it will be auto-generated by the database
        data.pop('id', None)
        
        # Convert date and time strings to datetime objects
        data['depurture_time'] = datetime.strptime(data['depurture_time'], '%Y-%m-%dT%H:%M:%S')
        data['arrival_time'] = datetime.strptime(data['arrival_time'], '%Y-%m-%dT%H:%M:%S')
        
        new_service = Travelling_service(**data)
        db.session.add(new_service)
        db.session.commit()
        return jsonify(new_service.to_dict()), 201
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"error": str(e)}), 400


# Route to update an existing travel service
@traveling_service_bp.route('/travel/<int:service_id>', methods=['PUT', 'PATCH'])
def update_travel_service(service_id):
    service = Travelling_service.query.get_or_404(service_id)
    data = request.json
    
    # Convert 'depurture_time' and 'arrival_time' strings to datetime objects
    depurture_time = datetime.strptime(data['depurture_time'], '%Y-%m-%d %H:%M:%S')
    arrival_time = datetime.strptime(data['arrival_time'], '%Y-%m-%d %H:%M:%S')
    
    # Update the service object with the new values
    service.name = data.get('name', service.name)
    service.depurture_time = depurture_time
    service.arrival_time = arrival_time
    service.price = data.get('price', service.price)
    service.seats = data.get('seats', service.seats)
    service.description = data.get('description', service.description)
    service.depurture_city = data.get('depurture_city', service.depurture_city)
    service.arrival_city = data.get('arrival_city', service.arrival_city)
    service.registration_number = data.get('registration_number', service.registration_number)
    
    
    # Commit the changes to the database
    db.session.commit()
        
    # Serialize the updated service object
    serialized_service = {
        "id": service.id,
        "name": service.name,
        "seats": service.seats,
        "depurture_time": service.depurture_time.strftime('%Y-%m-%d %H:%M:%S'),
        "arrival_time": service.arrival_time.strftime('%Y-%m-%d %H:%M:%S'),
        "description": service.description,
        "price": service.price,
        "depurture_city": service.depurture_city,
        "arrival_city": service.arrival_city,
        "registration_number": service.registration_number,
        "company_id": service.company_id
    }
    
    # Return the serialized service as JSON response
    return jsonify(serialized_service)

# Route to delete an existing travel service

# Delete needs reviews to be created so as to function

# @traveling_service_bp.route('/travel/<int:service_id>', methods=['DELETE'])
# def delete_travel_service(service_id):
#     service = Travelling_service.query.get_or_404(service_id)
#     db.session.delete(service)
#     db.session.commit()
#     return jsonify({'message': 'Travel service deleted successfully'}), 200



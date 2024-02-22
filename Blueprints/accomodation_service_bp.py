from flask import Blueprint, jsonify, request
from models import db, Accomodation_service

# Create a Blueprint for service routes

accomodation_service_bp = Blueprint('accomodation_service_bp', __name__)

# Route to get all accommodation services
@accomodation_service_bp.route('/accommodation', methods=['GET'])
def get_accommodation_services():
    accommodation_services = Accomodation_service.query.all()
    serialized_services = []
    for service in accommodation_services:
        serialized_service = {
            'id': service.id,
            'name': service.name,
            'location': service.location,
            'available_rooms': service.available_rooms,
            'images': service.images,
            'price_per_night': service.price_per_night,
            'average_rating': service.average_rating,
            'company_id': service.company_id
        }
        serialized_services.append(serialized_service)
    return jsonify(serialized_services)

# Route to get a single accommodation service by ID
@accomodation_service_bp.route('/accommodation/<int:service_id>', methods=['GET'])
def get_accommodation_service(service_id):
    service = Accomodation_service.query.get_or_404(service_id)
    serialized_service = {
        'id': service.id,
        'name': service.name,
        'location': service.location,
        'available_rooms': service.available_rooms,
        'images': service.images,
        'price_per_night': service.price_per_night,
        'average_rating': service.average_rating,
        'company_id': service.company_id
    }
    return jsonify(serialized_service)



# Route to create a new accommodation service
@accomodation_service_bp.route('/accommodation', methods=['POST'])
def create_accommodation_service():
    data = request.json
    new_service = Accomodation_service(**data)
    db.session.add(new_service)
    db.session.commit()
    return jsonify(new_service.to_dict()), 201

# Route to update an existing accommodation service
@accomodation_service_bp.route('/accommodation/<int:service_id>', methods=['PUT', 'PATCH'])
def update_accommodation_service(service_id):
    service = Accomodation_service.query.get_or_404(service_id)
    data = request.json
    for key, value in data.items():
        setattr(service, key, value)
    db.session.commit()
    
    # Manually serialize the updated service object
    serialized_service = {
        'id': service.id,
        'name': service.name,
        'location': service.location,
        'available_rooms': service.available_rooms,
        'images': service.images,
        'price_per_night': service.price_per_night,
        'average_rating': service.average_rating,
        'company_id': service.company_id
    }
    
    return jsonify(serialized_service)
# Route to delete an existing accommodation service
@accomodation_service_bp.route('/accommodation/<int:service_id>', methods=['DELETE'])
def delete_accommodation_service(service_id):
    service = Accomodation_service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'message': 'Accommodation service deleted successfully'}), 200





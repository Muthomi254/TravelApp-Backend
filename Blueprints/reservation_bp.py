from flask import Blueprint, jsonify, request
from models import db, Reservation_travel, Reservation_accomodation,User
from datetime import datetime

reservation_bp = Blueprint("reservation", __name__)

@reservation_bp.route('/reservations/accomodation', methods=['GET'])
def get_accomodation_reservations():
    reservations = Reservation_accomodation.query.all()

    reservation_list = []

    for reservation in reservations:
        reservation_dict = {
            "id": reservation.id,
            "user_email": reservation.user.email,
            "checkin": str(reservation.checkin),  
            "checkout": str(reservation.checkout), 
            "days_in_room": reservation.days_in_room,
            "price_net": (reservation.price_net),
            "user_id": reservation.user.id
        }
        reservation_list.append(reservation_dict)

    return jsonify(reservation_list)

@reservation_bp.route('/reservations/accomodation/<int:reservation_id>', methods=['GET'])
def get_accomodation_reservation_by_id(reservation_id):
    reservation = Reservation_accomodation.query.get_or_404(reservation_id)
    return jsonify({
            "id": reservation.id, 
            "user_email": reservation.user.email,  
            "checkin": (reservation.checkin), 
            "checkout": (reservation.checkout),
            "days_in_room": reservation.days_in_room,
            "price_net": (reservation.price_net),
            "user_id": reservation.user.id,
            "rooms":reservation.rooms,
            "people_included": reservation.people_included
                        
        })
@reservation_bp.route('/reservations/accomodation', methods=['POST'])
def create_accomodation_reservation():
    
    data = request.get_json()
    
    # reservation = Reservation_travel(**data)
    
    
    checkin=data['checkin']
    checkin=datetime.strptime(checkin, '%Y-%m-%d')
    checkout=data['checkout']
    checkout=datetime.strptime(checkout,'%Y-%m-%d')
    days_in_room=abs((checkout - checkin).days)+1
    user_id=data['user_id']
    rooms=data['rooms']
    people_included=data["people_included"]
    # calculations will be done in the front end
    price_net=data['price_net']
    
    
    new_reservation=Reservation_accomodation(checkin=checkin,checkout=checkout,days_in_room=days_in_room,user_id=user_id,price_net=price_net,rooms=rooms,people_included=people_included)
    
    if User.query.filter_by(id=user_id).first() is None :
        return jsonify({"error":"User does not exist"}), 404
    else:
        db.session.add(new_reservation)
        db.session.commit()
        return(jsonify({"message":"Reservation created successfully"}), 201)
    
            
        
@reservation_bp.route('/reservations/accomodation/<int:reservation_id>', methods=['PUT'])
def update_accomodation_reservation(reservation_id):
    reservation = Reservation_accomodation.query.get_or_404(reservation_id)
    data = request.get_json()
    if reservation:
        if data:
            if 'checkin' in data:
                checkin_data = data['checkin']
                checkin = datetime.strptime(checkin_data, '%Y-%m-%d')
                reservation.checkin = checkin
            elif 'checkout' in data:
                checkout_data = data['checkout']
                checkout = datetime.strptime(checkout_data, '%Y-%m-%d')
                reservation.checkout = checkout
            elif 'people_included' in data:
                people_included = data['people_included']
                reservation.people_included = people_included
            else:
                return jsonify({"error": "Missing field"}), 400

            # Ensure both checkin and checkout are of type datetime
            if hasattr(reservation.checkin, 'date') and hasattr(reservation.checkout, 'date'):
                # Convert datetime to date
                reservation.checkin = reservation.checkin.date()
                reservation.checkout = reservation.checkout.date()

                days_in_room = abs((reservation.checkout - reservation.checkin).days) + 1
                reservation.days_in_room = days_in_room
                price_net = data['price_net']
                reservation.price_net = price_net
            try:
                db.session.commit()
                return jsonify({"message": "reservation updated successfully"})
            except Exception as e:
                print(f"Error updating reservation: {e}")
                db.session.rollback()  # Rollback changes to avoid inconsistent state
                return jsonify({"error": "Failed to update reservation"}), 500
            # Delete a specific reservation by its id (for accommodations)
        else:
            return jsonify( {'error': 'No data provided'} ), 400
    else:
        return jsonify( { 'error': 'The specified reservation does not exist.'} ) , 404

@reservation_bp.route('/reservations/accomodation/<int:reservation_id>', methods=['DELETE'])
def delete_accomodation_reservation(reservation_id):
    reservation = Reservation_accomodation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation deleted successfully"})




# Similar routes for travels reservations


# @reservation_bp.route('/reservations/travel', methods=['GET'])
# def get_accomodation_travel():
#     reservations = Reservation_travel.query.all()
#     return jsonify([reservation.to_dict() for reservation in reservations])


@reservation_bp.route('/reservations/travel/<int:reservation_id>', methods=['DELETE'])
def delete_travel_reservation(reservation_id):
    reservation = Reservation_travel.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation deleted successfully"})

@reservation_bp.route('/reservations/travel', methods=['GET'])
def get_travel_reservations():
    reservations = Reservation_travel.query.all()

    reservation_list = []

    for reservation in reservations:
        reservation_dict = {
            "id": reservation.id,
            "user_email": reservation.user.email,
            "date": reservation.date,
            "user_id": reservation.user.id
        }
        reservation_list.append(reservation_dict)

    return jsonify(reservation_list)

@reservation_bp.route('/reservation/travel/<int:user_id>', methods=['GET'])
def get_travel_reservation_by_id(user_id):
    reservation= Reservation_travel.query.filter_by(user_id=user_id).first()
    if reservation:
        return jsonify({
            "id": reservation.id,
            "user_email": reservation.user.email,
            "date": reservation.date,
            "user_id": reservation.user.id
        })

@reservation_bp.route("/reservation/travel", methods=["POST"])
def  add_travel_reservation():
    data=request.get_json()
    user_id=data['user_id']
    people_included=data['people_included']
    date=datetime.strptime(data['date'],'%Y-%m-%d')
    try:
        new_reservation=Reservation_travel(user_id=user_id,people_included=people_included,date=date)
        db.session.add(new_reservation)
        db.session.commit()
        return jsonify({"message":"The travel reservation was added successfuly"}),201
    except Exception as e:
        return {"error":"There was an error with your request."},500
    
@reservation_bp.route("/reservation/travel/<int:reservation_id>",methods=['PUT'])
def  update_travel_reservation(reservation_id):
    data=request.get_json()
    reservation=Reservation_travel.query.filter_by(id=reservation_id).first()
    if reservation:
        if 'user_id' in data :
            reservation.user_id=data['user_id']
        elif  'people_included' in data:
            reservation.people_included=data['people_included']
        elif  'date' in data:
            reservation.date=datetime.strptime(data['date'],'%Y-%m-%d')
    else:
        return jsonify({"message":"No reservation found with given id"}),404
    db.session.commit()
    return jsonify({"message":"The travel reservation has been updated"}),200  
            
    
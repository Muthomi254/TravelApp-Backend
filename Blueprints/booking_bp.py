from flask import Blueprint,jsonify,request
from models import Travel_booking,Accomodation_booking,User,db,Reservation_travel,Travelling_service,Reservation_accomodation,Accomodation_service
from flask_jwt_extended import jwt_required, get_jwt_identity


booking_bp=Blueprint("booking",__name__)

@booking_bp.route("/travel/bookings",methods=['GET'])
def get_book_travel():
    bookings=Travel_booking.query.all()
    booking_list=[]
    for booking in  bookings:
        booking_dict={
            "id":booking.id,
            "user_email":booking.travelling_reservation.user.email,
            "depurture_city":booking.travelling_service.depurture_city,
            "arrival_city":booking.travelling_service.arrival_city,
            "depurture_time":str(booking.travelling_service.depurture_time),
            "price":booking.travelling_service.price
        }
        booking_list.append(booking_dict)
    
    if booking_list:
            return jsonify({"status": "success", "bookings": booking_list})
    else:
            return jsonify(message="No travel booking yet")
    
@booking_bp.route("/travel/bookings/<int:booking_id>", methods=['GET'])
def get_travel_booking_by_id(booking_id):
    booking = Travel_booking.query.get(booking_id)

    if booking:
        booking_dict = {
            "id": booking.id,
            "user_email": booking.travelling_reservation.user.email,
            "depurture_city": booking.travelling_service.depurture_city,
            "arrival_city": booking.travelling_service.arrival_city,
            "depurture_time": str(booking.travelling_service.depurture_time),
            "price": booking.travelling_service.price
        }

        return jsonify({"status": "success", "booking": booking_dict})
    else:
        return jsonify({"error": f"Travel booking with ID {booking_id} not found"}), 404


@booking_bp.route("/accomodation/bookings",methods=['GET'])
def get_book_accomodation():
    bookings=Accomodation_booking.query.all()
    booking_list=[]
    if bookings:
        for booking in  bookings:
            booking_dict={
                "id":booking.id,
                "user_email":booking.accomodation_reservation.user.email,
                "depurture_city":booking.accomodation_service.depurture_city,
                "arrival_city":booking.accomodation_service.arrrival_city,
                "depurture_time":str(booking.accomodation_reservation.depurture_time),
                "price":booking.accomodation_service
            }
        booking_list.append(booking_dict)
        return jsonify(bookings=booking_list)

    else:
        return jsonify(message="No accomdation booking yet")
    
@booking_bp.route('/<string:type>/bookings/add',methods=["POST"])
@jwt_required()
def  add_a_new_booking(type):
    user=User.query.filter_by(id=get_jwt_identity()).first()
    # return get_jwt_identity()
    
    if user:
        data=request.get_json()
        
            

        if  type=="travel":
            if Reservation_travel.query.filter_by(id=data['travelling_reservation_id']).count()>0 and Travelling_service.query.filter_by(id=data["travelling_service_id"]):

                travelling_reservation_id=data["travelling_reservation_id"]
                travelling_service_id=data["travelling_service_id"]
                new_booking=Travel_booking(travelling_reservation_id=travelling_reservation_id,travelling_service_id=travelling_service_id)
                db.session.add(new_booking)
                db.session.commit()
                return jsonify(status='success', message = 'Booking added successfully')
            else:
                return jsonify({"error":"cannot find the travel reservation  or service"}),400

        elif  type=="accommodation":
            if  Reservation_accomodation.query.filter_by(id=int(data['accommodation_reservation_id'])).first() and Accomodation_service.query.filter_by(id=data['accomodation_service_id']):
                accomodation_reservation_id=data["accomodation_reservation_id"]
                accomodation_service_id=data["accomodation_service_id"]
                new_booking= Accomodation_booking(accomodation_reservation_id=accomodation_reservation_id ,accomodation_service_id=accomodation_service_id)
                db.session.add(new_booking)
                db.session.commit()
                return jsonify(status='success', message = 'Booking added successfully')
        else :
            return jsonify({"error":"Invalid Booking Type"}),400

        
        # else:
        #     return jsonify("Invalid Booking Type"),400
    else:
        return jsonify({"message":"You are not logged in"}),401
                
@booking_bp.route('/travel/bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def delete_travel_booking(booking_id):
    user = User.query.filter_by(id=get_jwt_identity()).first()

    if user:
        travel_booking = Travel_booking.query.get(booking_id)

        if travel_booking:
            db.session.delete(travel_booking)
            db.session.commit()
            return jsonify(status='success', message='Booking deleted successfully')
        else:
            return jsonify({"error": "Travel booking not found"}), 404
    else:
        return jsonify({"message": "You are not logged in"}), 401


@booking_bp.route('/accommodation/bookings/<int:booking_id>', methods=['DELETE'])
@jwt_required()
def delete_accommodation_booking(booking_id):
    user = User.query.filter_by(id=get_jwt_identity()).first()

    if user:
        accommodation_booking = Accomodation_booking.query.get(booking_id)

        if accommodation_booking:
            db.session.delete(accommodation_booking)
            db.session.commit()
            return jsonify(status='success', message='Booking deleted successfully')
        else:
            return jsonify({"error": "Accommodation booking not found"}), 404
    else:
        return jsonify({"message": "You are not logged in"}), 401
        
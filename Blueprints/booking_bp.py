from flask import Blueprint,jsonify,request
from models import Travel_booking,Accomodation_booking,User,db
from flask_jwt_extended import jwt_required, get_jwt_identity


booking_bp=Blueprint("booking",__name__)

@booking_bp.route("/travel/bookings",methods=['GET'])
def book_travel():
    bookings=Travel_booking.query.all()
    booking_list=[]
    if bookings:
        for booking in  bookings:
            booking_dict={
                "id":booking.id,
                "user_email":booking.travelling_reservation.user.email,
                "depurture_city":booking.travelling_service.depurture_city,
                "arrival_city":booking.travelling_service.arrrival_city,
                "depurture_time":str(booking.travelling_reservation.depurture_time),
                "price":booking.travelling_service
            }
            booking_list.append(booking_dict)
        return jsonify(bookings=booking_list)

    else:
        return jsonify(message="No travel booking yet")

@booking_bp.route("/accomodation/bookings",methods=['GET'])
def book_accomodation():
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
    
@jwt_required()
@booking_bp.route('/<string:type>/bookings/add',methods=["POST"])
def  add_a_new_booking(type):
    user=User.query.filter_by(email=get_jwt_identity()).first()

    
    if user:
        data=request.get_json()

        if  type=="Travel":
            travelling_reservation_id=data["travelling_reservation_id"]
            travelling_service_id=data["travelling_service_id"]
            new_booking=Travel_booking(travelling_reservation_id,travelling_service_id)
            db.session.add(new_booking)
            return jsonify(status='success', message = 'Booking added successfully')

        elif  type=="Accommodation":
            accomodation_reservation_id=data["accomodation_reservation_id"]
            accomodation_service_id=data["accomodation_service_id"]
            new_booking= Accomodation_booking(accomodation_reservation_id ,accomodation_service_id )
            db.session.add(new_booking)
            db.session.commit()
            return jsonify(status='success', message = 'Booking added successfully')

        
        else:
            return jsonify("Invalid Booking Type"),400
    else:
        return jsonify({"message":"You are not logged in"}),401
                
        
        
import hashlib
from flask_login import current_user
from hotelmanagement import db, app
from hotelmanagement.models import Room, TypeRoom, User, UserRole, Receipt, ReceiptDetail, ReservationDetail, \
    Reservation
from sqlalchemy import func
from sqlalchemy.sql import extract


def load_typeroom():
    return TypeRoom.query.all()


def load_room(tyroom_id=None, kw=None, from_price=None, to_price=None):
    rooms = Room.query.filter(Room.active.__eq__(True))

    if tyroom_id:
        rooms = rooms.filter(Room.typeroom_id.__eq__(tyroom_id))

    if kw:
        rooms = rooms.filter(Room.name.contains(kw))

    if from_price:
        rooms = rooms.filter(Room.price.__ge__(float(from_price)))

    if to_price:
        rooms = rooms.filter(Room.price.__le__(float(to_price)))

    return rooms


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(), username=username.strip(), password=password, email=kwargs.get('email'),
                phone=kwargs.get('phone'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_login_customer(username, password, role=UserRole.CUSTOMER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def check_login_staff(username, password, role=UserRole.STAFF):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def check_login_admin(username, password, role=UserRole.ADMIN):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def get_room_by_id(room_id):
    return Room.query.get(room_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)


def add_receipt(booking):
    if booking:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for b in booking.values():
            d = ReceiptDetail(receipt=receipt,
                              room_id=b['id'],
                              # cus_name=b['cus_name'],
                              # checkin_date=b['checkin_date'],
                              # checkout_date=b['checkout_date'],
                              quantity=b['quantity'],
                              unit_price=b['price'])
            db.session.add(d)
        db.session.commit()


def count_booking(booking):
    total_quantity, total_amount = 0, 0

    if booking:
        for b in booking.values():
            total_quantity += b['quantity']
            total_amount += b['quantity'] * b['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }


def typeroom_stats(): #danhsachphong
    return db.session.query(Room.id, Room.name, TypeRoom.name, Room.price, Room.active) \
        .join(Room, TypeRoom.id.__eq__(Room.typeroom_id), isouter=True) \
        .group_by(Room.id, Room.name, TypeRoom.name, Room.price, Room.active).all()





def used_room_stats(month): #matdosudungphong theo thang thieu' so ngay thue
    return db.session.query(Room.id, Room.name,
                            ReceiptDetail.quantity / Room.available_room) \
        .join(Room, ReceiptDetail.room_id.__eq__(Room.id)) \
        .join(Receipt, ReceiptDetail.receipt_id.__eq__(Receipt.id)) \
        .filter(extract('month', Receipt.created_date) == month) \
        .group_by(Room.id, Room.name, ReceiptDetail.quantity / Room.available_room).all()


def month_stats(month):  #doanhthuthang index
    return db.session.query(TypeRoom.name, Room.name,
                            func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price).label('sales'),
                            ReceiptDetail.quantity, ReceiptDetail.quantity / Room.available_room, func.sum('sales')) \
        .join(Room, TypeRoom.id.__eq__(Room.typeroom_id), isouter=True) \
        .join(ReceiptDetail, ReceiptDetail.room_id.__eq__(Room.id)) \
        .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id)) \
        .filter(extract('month', Receipt.created_date) == month) \
        .group_by(TypeRoom.name, Room.name, ReceiptDetail.quantity, ReceiptDetail.quantity / Room.available_room).all()



def room_month_stats(month): # tong doanh thu index
    return db.session.query(extract('month', Receipt.created_date),
                            func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price)) \
        .join(ReceiptDetail, ReceiptDetail.receipt_id.__eq__(Receipt.id)) \
        .filter(extract('month', Receipt.created_date) == month) \
        .group_by(extract('month', Receipt.created_date)).order_by(extract('month', Receipt.created_date)).all()


def add_reservation(orderer, room_id, checkin_date, checkout_date, customer1, customer2, customer3):
    if customer1 and customer2 and customer3:
        rs = Reservation(rsuser=current_user,
                         room_id=room_id,
                         orderer=orderer,
                         checkin_date=checkin_date,
                         checkout_date=checkout_date)
        db.session.add(rs)

        dt = ReservationDetail(reservation=rs,
                               cus_name=customer1['cus_name'],
                               typeguest_id=customer1['type_guest'],
                               id_card=customer1['id_card'],
                               address=customer1['address'])
        db.session.add(dt)

        dt2 = ReservationDetail(reservation=rs,
                                cus_name=customer2['cus_name'],
                                typeguest_id=customer2['type_guest'],
                                id_card=customer2['id_card'],
                                address=customer2['address'])
        db.session.add(dt2)

        dt3 = ReservationDetail(reservation=rs,
                                cus_name=customer3['cus_name'],
                                typeguest_id=customer3['type_guest'],
                                id_card=customer3['id_card'],
                                address=customer3['address'])
        db.session.add(dt3)
        db.session.commit()


def show_rent(id):
    return db.session.query(ReservationDetail.id, ReservationDetail.cus_name, ReservationDetail.typeguest_id,
                            ReservationDetail.id_card,
                            ReservationDetail.address) \
        .join(Reservation, ReservationDetail.reservation_id.__eq__(Reservation.id), isouter=True) \
        .filter(ReservationDetail.reservation_id == id) \
        .group_by(ReservationDetail.id,
                  ReservationDetail.cus_name, ReservationDetail.typeguest_id, ReservationDetail.id_card,
                  ReservationDetail.address).all()


def show_rent2(id):
    return db.session.query(Reservation.room_id, Reservation.checkin_date, Reservation.checkout_date) \
        .filter(Reservation.id == id) \
        .group_by(Reservation.room_id, Reservation.checkin_date, Reservation.checkout_date).all()


def show_booking():
    return db.session.query(Reservation.checkin_date, Reservation.checkout_date) \
        .group_by(Reservation.checkin_date, Reservation.checkout_date).all()

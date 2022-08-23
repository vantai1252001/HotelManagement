from sqlalchemy import Column, Integer, Enum, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from hotelmanagement import db
from datetime import datetime, date
from flask_login import UserMixin
from enum import Enum as UserEnum


class  BaseModel(db.Model):
    __abstract__ = True  # khong tao bang
    id = Column(Integer, primary_key=True, autoincrement=True)

# class BillModel(db.Model):
#     __abstract__ = True


class TypeRoom(BaseModel):
    __tablename__ = 'typeroom'

    name = Column(String(20), nullable=False)
    rooms = relationship("Room", backref="typeroom", lazy=False)  # many to one

    def __str__(self):
        return self.name


class Room(BaseModel):
    __tablename__ = 'room'
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)  # mac dinh la con ban hang
    created_date = Column(DateTime, default=datetime.now())
    available_room = Column(Integer, default=5)
    max_people = Column(Integer)
    size = Column(Float)
    typeroom_id = Column(Integer, ForeignKey(TypeRoom.id), nullable=False)  # ForeignKey('category_id)
    receipt_details = relationship('ReceiptDetail', backref='room', lazy=True)
    reservation = relationship('Reservation', backref='rsroom', lazy=True)

    def __str__(self):
        return self.name



class UserRole(UserEnum):
    ADMIN = 1
    CUSTOMER = 2
    STAFF = 3


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    phone = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    reservation = relationship('Reservation', backref='rsuser', lazy=True)

    def __str__(self):
        return self.name


class Reservation(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False)
    orderer = Column(String(50))
    checkin_date = Column(DateTime)
    checkout_date = Column(DateTime)
    details = relationship('ReservationDetail', backref='reservation', lazy=True)
    # receipt = relationship('Receipt', backref='rsreceipt', lazy=True)


class TypeGuest(BaseModel):
    __tablename__ = 'typeguest'
    type = Column(String(20), nullable=False)
    reser_detail = relationship('ReservationDetail', backref='reserdetail', lazy=False)

    def __str__(self):
        return self.type


class ReservationDetail(BaseModel):
    reservation_id = Column(Integer, ForeignKey(Reservation.id), nullable=False, primary_key=True)

    cus_name = Column(String(50), nullable=False)
    typeguest_id = Column(Integer, ForeignKey(TypeGuest.id), nullable=False)
    id_card = Column(String(20), nullable=False)
    address = Column(String(100))


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)
    # reservation = Column(Integer, ForeignKey(Reservation.id), nullable=True)


class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    room_id = Column(Integer, ForeignKey(Room.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


if __name__ == '__main__':
     #db.create_all()

    tp1 = TypeGuest(type='Nội địa')
    tp2 = TypeGuest(type='Nước ngoài')
    db.session.add(tp1)
    db.session.add(tp2)
    db.session.commit()
    t1 = TypeRoom(name='Thường')
    t2 = TypeRoom(name='Vip')
    t3 = TypeRoom(name='Luxury')
    db.session.add(t1)
    db.session.add(t2)
    db.session.add(t3)
    db.session.commit()

    rooms = [{
        "id": 1,
        "name": "KING SUITE ROOM",
        "description": "Experience our spacious 28 sqm Superior room, with a unique interior design that creates a relaxing and elegant ambience.",
        "price": 68,
        "image": "images/p1.jpg",
        "available_room": "5",
        "max_people": 3,
        "size": 22,
        "typeroom_id": 1
    }, {
        "id": 2,
        "name": "QUEEN SUITE ROOM",
        "description": "Offering fantastic views of Hanoi city featuring 30 sqm, this Spacious Deluxe offers an abundance of space for business or relaxation.",
        "price": 78,
        "image": "images/p1.jpg",
        "available_room": "5",
        "max_people": 3,
        "size": 22,
        "typeroom_id": 2
    }, {
        "id": 3,
        "name": "LUXURY SUITE",
        "description": "Triple Rooms in our hotel are available with three single beds, perfectly equipped for traveling friends or business partners. An elegant bathroom with shower is included in the room. The rooms offer you all home comfort, complete your travel experiences",
        "price": 100,
        "image": "images/p1.jpg",
        "available_room": "5",
        "max_people": 3,
        "size": 22,
        "typeroom_id": 3
    }, {
        "id": 4,
        "name": "Luxury Villa Poolside",
        "description": "Offering fantastic views of Hanoi city featuring 30 sqm, this Spacious Deluxe offers an abundance of space for business or relaxation.",
        "price": 72,
        "image": "images/p1.jpg",
        "available_room": "5",
        "max_people": 5,
        "size": 32,
        "typeroom_id": 3
    }, {
        "id": 5,
        "name": "Premium Deluxe Ocean View",
        "description": "Offering fantastic views of Hanoi city featuring 30 sqm, this Spacious Deluxe offers an abundance of space for business or relaxation.",
        "price": 62,
        "image": "images/p1.jpg",
        "available_room": "5",
        "max_people": 4,
        "size": 24,
        "typeroom_id": 2
    }]
    for r in rooms:
        ro = Room(name=r['name'], price=r['price'], image=r['image'], available_room=r['available_room'],description=r['description'],
                   typeroom_id=r['typeroom_id'], max_people=r['max_people'], size=r['size'])
        db.session.add(ro)
    db.session.commit()

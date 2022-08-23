import datetime

from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify
import cloudinary.uploader
import string
from hotelmanagement import app, login
from flask_login import login_user, logout_user, login_required
import utils
from hotelmanagement.models import UserRole


@app.route("/")
def index():
    tyroom_id = request.args.get("typeroom_id")
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    # page = request.args.get('page', 1)
    rooms = utils.load_room(tyroom_id=tyroom_id, kw=kw, from_price=from_price, to_price=to_price)
    return render_template('index.html', rooms=rooms)


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        confirm = request.form.get('confirm')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name, username=username, password=password, email=email, phone=phone,
                               avatar=avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg = "Mật khẩu không khớp"
        except Exception as ex:
            err_msg = "Hệ thống đang có lỗi!!!" + str(ex)
    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            user = utils.check_login_customer(username=username, password=password, role=UserRole.CUSTOMER)

            if user:
                login_user(user=user)
                next = request.args.get('next', 'index')
                return redirect(url_for(next))
            else:
                user = utils.check_login_staff(username=username, password=password)
                if user:
                    login_user(user=user)
                    next = request.args.get('next', 'index')
                    return redirect(url_for(next))
                else:
                    err_msg = "Tài khoản hoặc mật khẩu không chính xác!!"
        except Exception as ex:
            err_msg = str(ex)

    return render_template('login.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_login_admin(username=username, password=password, role=UserRole.ADMIN)
    if user:
        login_user(user=user)
        return redirect('/admin')
    else:
        # messages = json.dumps({"main": "Condition failed on page baz"})
        #
        # return redirect(url_for('.do_foo', messages=messages))
        # messages = 'Tài khoản hoặc mật khẩu không chính xác!!!'
        # session['messages'] = messages
        flash('Tài khoản của bạn không có quyền quản trị')
        return redirect(url_for('admin.index'))


@app.route('/products/<int:room_id>')
def room_details(room_id):
    room = utils.get_room_by_id(room_id)

    return render_template('roomdetails.html', room=room)


@app.route('/reservation', methods=['get', 'post'])
def reservation():
    if request.method.__eq__('POST'):
        orderer = request.form.get('orderer')
        room_id = request.form.get('room_id')
        checkin_date = request.form.get('checkin_date')
        checkout_date = request.form.get('checkout_date')
        cus_name = request.form.get('cus_name')
        type_guest = request.form.get('type_guest')
        id_card = request.form.get('id_card')
        address = request.form.get('address')
        cus_name2 = request.form.get('cus_name2')
        type_guest2 = request.form.get('type_guest2')
        id_card2 = request.form.get('id_card2')
        address2 = request.form.get('address2')
        cus_name3 = request.form.get('cus_name3')
        type_guest3 = request.form.get('type_guest3')
        id_card3 = request.form.get('id_card3')
        address3 = request.form.get('address3')

        customer1 = {
            'cus_name': cus_name,
            'type_guest': type_guest,
            'id_card': id_card,
            'address': address
        }
        customer2 = {
            'cus_name': cus_name2,
            'type_guest': type_guest2,
            'id_card': id_card2,
            'address': address2
        }
        customer3 = {
            'cus_name': cus_name3,
            'type_guest': type_guest3,
            'id_card': id_card3,
            'address': address3
        }

        utils.add_reservation(orderer=orderer,
                              room_id=room_id,
                              checkin_date=checkin_date,
                              checkout_date=checkout_date,
                              customer1=customer1,
                              customer2=customer2,
                              customer3=customer3)

    return render_template('reservation.html')


# @app.route('/products/<int:room_id>')
# def payment(room_id):
#     room = utils.get_room_by_id(room_id)
#
#     return render_template('roomdetails.html', room=room)


@app.route('/booking')
def booking():
    show_booking = utils.show_booking()
    return render_template('booking.html', show_booking=show_booking, count=utils.count_booking(session.get('booking')))


@app.route('/rent')
def rent():
    id = request.args.get('id')
    show_rent = utils.show_rent(id)
    show_rent2 = utils.show_rent2(id)
    return render_template('rent.html', show_rent=show_rent, show_rent2=show_rent2)


@app.route('/api/add-booking', methods=['POST'])
def add_to_booking():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    # checkin_d = data.get(checkin_date)
    # checkout_d = data.get(checkout_date)

    booking = session.get('booking')
    if not booking:
        booking = {}

    if id in booking:
        booking[id]['quantity'] = booking[id]['quantity'] + 1

    else:
        booking[id] = {
            'id': id,
            'name': name,
            # 'checkin_date': checkin_d,
            # 'checkout_date': checkout_d,
            'price': price,
            'quantity': 1
        }
    session['booking'] = booking

    return jsonify(utils.count_booking(booking))


@app.route('/api/update-booking', methods=['put'])
def update_booking():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    booking = session.get('booking')

    if booking and id in booking:
        booking[id]['quantity'] = quantity
        session['booking'] = booking

    return jsonify(utils.count_booking(booking))


@app.route('/api/delete-cart/<room_id>', methods=['delete'])
def delete_cart(room_id):
    booking = session.get('booking')
    if booking and room_id in booking:
        del booking[room_id]
        session['booking'] = booking
    return jsonify(utils.count_booking(booking))


@app.route('/api/pay', methods=['POST'])
@login_required
def pay():
    if request.method.__eq__('POST'):
        # cus_name = request.form.get('name')
        try:
            utils.add_receipt(session.get('booking'))
            del session['booking']

        except:
            return jsonify({'code': 400})

    return jsonify({'code': 200})


@app.route('/user-logout')
def user_logout():
    logout_user()
    return redirect(url_for('user_signin'))


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.context_processor
def common_response():
    return {
        'typerooms': utils.load_typeroom(),
        'booking_stats': utils.count_booking(session.get('booking'))
    }


if __name__ == '__main__':
    from hotelmanagement.admin import *

    app.run(debug=True)

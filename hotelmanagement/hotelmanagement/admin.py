from hotelmanagement import app, db

from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_login import current_user, logout_user
from flask_admin.contrib.sqla import ModelView
from hotelmanagement.models import Room, TypeRoom, User, UserRole
from flask import redirect
import utils
from flask import request
from datetime import datetime


class AuthenModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class RoomView(AuthenModelView):
    column_display_pk = True  # hien khoa chinh
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'active', ' created_date']  # an label
    column_labels = {
        'name': 'Tên phòng',
        'description': 'Mô tả',
        'price': 'Giá',
        'image': 'Ảnh đại diện',
        'typeroom': "Loại phòng",
        'max_people': "Số lượng người tối đa",
        'size': "Kích thước phòng",
        'created_date': 'Ngày tạo'
    }
    column_sortable_list = ['name', 'price', 'id']  # cho sap xep theo ten,gia,id


class TypeRoomView(AuthenModelView):
    column_labels = {
        'name': 'Loại phòng'
    }


class Logout(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        month = request.args.get('month', datetime.now().month)
        return self.render('admin/stats.html'
                           , stats=utils.typeroom_stats(), statss=utils.used_room_stats(month=month))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        month = request.args.get('month', datetime.now().month)
        return self.render('admin/index.html', stats=utils.month_stats(month=month), statss=utils.room_month_stats(month=month))


admin = Admin(app=app, name="Hotel Management Administration", template_mode='bootstrap4', index_view=MyAdminIndex())
admin.add_view(AuthenModelView(TypeRoom, db.session))
admin.add_view(RoomView(Room, db.session))
admin.add_view(StatsView(name='Stats'))
admin.add_view(Logout(name='Logout'))

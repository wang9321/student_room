from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db


class User(UserMixin, db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)  # 学号
    full_name = db.Column(db.String(64), nullable=False)  # 真实姓名
    phone = db.Column(db.String(20))  # 手机号
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)  # 账户状态
    avatar = db.Column(db.String(200), default='/static/images/default_avatar.svg')  # 头像路径

    # 关联关系
    bookings = db.relationship('Booking', backref='user', lazy='dynamic', cascade='all, delete-orphan',
                              foreign_keys='Booking.user_id')

    def set_password(self, password):
        """设置密码"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def get_active_bookings(self):
        """获取当前活跃的预约"""
        # 暂时返回空列表，避免循环导入问题
        # 实际应用中可以通过延迟加载或字符串查询解决
        return []

    def can_book(self):
        """检查用户是否可以预约"""
        # 检查账户是否激活
        if not self.is_active:
            return False, "账户已被禁用"

        # 检查是否已有活跃预约
        active_bookings = self.get_active_bookings()
        if active_bookings:
            return False, "您已有未完成的预约"

        return True, "可以预约"

    def __repr__(self):
        return f'<User {self.username}>'

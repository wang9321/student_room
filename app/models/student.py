from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class Student(db.Model, UserMixin):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)  # 学号
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))  # 性别
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    major = db.Column(db.String(100))  # 专业
    grade = db.Column(db.String(10))   # 年级
    class_name = db.Column(db.String(50))  # 班级
    avatar = db.Column(db.String(200))
    status = db.Column(db.String(20), default='active')  # active, suspended
    credit_score = db.Column(db.Integer, default=100)  # 信用积分
    total_bookings = db.Column(db.Integer, default=0)
    violation_count = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

    def can_book(self):
        """检查学生是否可以预约"""
        return (self.status == 'active' and
                self.is_active and
                self.credit_score >= 80)

    def update_credit_score(self, change, reason=None):
        """更新信用积分"""
        self.credit_score += change
        if self.credit_score < 0:
            self.credit_score = 0
        elif self.credit_score > 100:
            self.credit_score = 100

    def __repr__(self):
        return f'<Student {self.student_id} - {self.name}>'

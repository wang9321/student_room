from datetime import datetime

from app import db


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_number = db.Column(db.String(30), unique=True, nullable=False, index=True)  # 预约编号
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('seats.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)  # 预约日期
    start_time = db.Column(db.DateTime, nullable=False)  # 开始时间
    end_time = db.Column(db.DateTime, nullable=False)    # 结束时间
    purpose = db.Column(db.String(200))  # 预约用途
    status = db.Column(db.String(20), default='active')  # active, cancelled, completed, no_show
    check_in_time = db.Column(db.DateTime)  # 签到时间
    check_out_time = db.Column(db.DateTime)  # 签退时间
    cancel_reason = db.Column(db.Text)  # 取消原因
    violation_type = db.Column(db.String(50))  # 违规类型
    notes = db.Column(db.Text)  # 备注
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Booking, self).__init__(**kwargs)
        if not self.booking_number:
            self.booking_number = self.generate_booking_number()

    @staticmethod
    def generate_booking_number():
        """生成预约编号"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        import random
        random_num = random.randint(1000, 9999)
        return f"CD{timestamp}{random_num}"

    @property
    def duration_hours(self):
        """预约时长(小时)"""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600

    @property
    def is_active_now(self):
        """检查预约是否当前有效"""
        now = datetime.utcnow()
        return (self.status == 'active' and
                self.start_time <= now <= self.end_time)

    def can_cancel(self):
        """检查是否可以取消预约"""
        if self.status not in ['active']:
            return False
        now = datetime.utcnow()
        # 至少提前30分钟取消
        return (self.start_time - now).total_seconds() >= 1800

    def check_in(self):
        """签到"""
        if self.status == 'active':
            self.check_in_time = datetime.utcnow()
            return True
        return False

    def check_out(self):
        """签退"""
        if self.status == 'active' and self.check_in_time:
            self.check_out_time = datetime.utcnow()
            self.status = 'completed'
            return True
        return False

    def cancel(self, reason=None):
        """取消预约"""
        if self.can_cancel():
            self.status = 'cancelled'
            self.cancel_reason = reason
            return True
        return False

    def mark_no_show(self):
        """标记为未到场"""
        if self.status == 'active':
            self.status = 'no_show'
            # 扣除信用积分
            if hasattr(self.user, 'update_credit_score'):
                self.user.update_credit_score(-10, '未到场预约')
            if hasattr(self.user, 'violation_count'):
                self.user.violation_count += 1
            return True
        return False

    @staticmethod
    def check_seat_availability(seat_id, start_time, end_time, exclude_booking_id=None):
        """检查座位在指定时间段是否可用"""
        query = Booking.query.filter(
            Booking.seat_id == seat_id,
            Booking.status.in_(['active', 'completed']),
            Booking.start_time < end_time,
            Booking.end_time > start_time
        )

        if exclude_booking_id:
            query = query.filter(Booking.id != exclude_booking_id)

        conflicting_booking = query.first()
        return conflicting_booking is None

    @staticmethod
    def update_expired_bookings():
        """更新过期的预约"""
        # 使用本地时间而不是UTC时间进行比较
        now = datetime.now()
        expired_bookings = Booking.query.filter(
            Booking.status == 'active',
            Booking.end_time < now
        ).all()

        for booking in expired_bookings:
            # 如果已经签到，则标记为已完成
            if booking.check_in_time:
                booking.status = 'completed'
                booking.check_out_time = booking.end_time  # 使用预约结束时间作为签退时间
            else:
                # 如果没有签到，则标记为未到场
                booking.status = 'no_show'

        if expired_bookings:
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise e

        return len(expired_bookings)

    @staticmethod
    def get_realtime_seat_usage():
        """获取实时座位使用情况"""
        from app import db
        now = datetime.now()

        # 获取当前时间段内的活跃预约对应的座位数
        occupied_seats = db.session.query(Booking.seat_id).filter(
            Booking.status == 'active',
            Booking.start_time <= now,
            Booking.end_time >= now
        ).distinct().count()

        return occupied_seats

    def __repr__(self):
        return f'<Booking {self.booking_number} - User {self.user_id}>'

class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publisher_type = db.Column(db.String(20), nullable=False)  # admin, system
    publisher_id = db.Column(db.Integer)  # 发布者ID
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    priority = db.Column(db.String(20), default='normal')  # high, normal, low
    target_audience = db.Column(db.String(50), default='all')  # all, students, admins
    is_active = db.Column(db.Boolean, default=True)
    view_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Announcement {self.title}>'

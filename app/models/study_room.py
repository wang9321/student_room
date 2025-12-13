from datetime import datetime

from app import db


class StudyRoom(db.Model):
    __tablename__ = 'study_rooms'

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    building = db.Column(db.String(50), nullable=False)  # 所属楼栋
    floor = db.Column(db.String(10))  # 楼层
    capacity = db.Column(db.Integer, nullable=False)  # 座位总数
    room_type = db.Column(db.String(30), default='regular')  # regular, quiet, discussion, computer
    description = db.Column(db.Text)
    location = db.Column(db.String(100))  # 位置描述
    facilities = db.Column(db.Text)  # 设施描述 JSON格式
    open_time = db.Column(db.String(20))  # 开放时间
    close_time = db.Column(db.String(20))  # 关闭时间
    image = db.Column(db.String(200))
    status = db.Column(db.String(20), default='open')  # open, closed, maintenance
    booking_rules = db.Column(db.Text)  # 预约规则

    # 设施标识
    has_power = db.Column(db.Boolean, default=True)  # 是否有电源
    has_wifi = db.Column(db.Boolean, default=True)  # 是否有WiFi
    has_air_conditioning = db.Column(db.Boolean, default=True)  # 是否有空调
    is_quiet = db.Column(db.Boolean, default=False)  # 是否为安静区域
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    seats = db.relationship('Seat', backref='study_room', lazy='dynamic')

    @property
    def available_seats_count(self):
        """可用座位数量（基于实时预约数据）"""
        from datetime import datetime
        from app import db
        from app.models.booking import Booking

        # 获取当前时间
        now = datetime.now()

        # 查询该房间当前被占用的座位
        occupied_seat_ids = db.session.query(Booking.seat_id).filter(
            Booking.seat_id.in_([s.id for s in self.seats]),
            Booking.status == 'active',
            Booking.start_time <= now,
            Booking.end_time >= now
        ).distinct().all()

        occupied_seat_ids = [s[0] for s in occupied_seat_ids]

        # 计算可用座位数
        return self.seats.filter(~Seat.id.in_(occupied_seat_ids)).count() if occupied_seat_ids else self.seats.count()

    @property
    def occupied_seats_count(self):
        """已占用座位数量（基于实时预约数据）"""
        from datetime import datetime
        from app import db
        from app.models.booking import Booking

        # 获取当前时间
        now = datetime.now()

        # 查询该房间当前被占用的座位数
        occupied_count = db.session.query(Booking.seat_id).filter(
            Booking.seat_id.in_([s.id for s in self.seats]),
            Booking.status == 'active',
            Booking.start_time <= now,
            Booking.end_time >= now
        ).distinct().count()

        return occupied_count

    def get_seats_by_type(self, seat_type):
        """根据类型获取座位"""
        return self.seats.filter_by(type=seat_type).all()

    def __repr__(self):
        return f'<StudyRoom {self.room_number} - {self.name}>'

class Seat(db.Model):
    __tablename__ = 'seats'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('study_rooms.id'), nullable=False)
    seat_number = db.Column(db.String(20), nullable=False)  # 座位编号
    type = db.Column(db.String(30), default='regular')  # regular, window, power, computer
    status = db.Column(db.String(20), default='available')  # available, occupied, maintenance
    power_socket = db.Column(db.Boolean, default=False)  # 是否有电源
    window_seat = db.Column(db.Boolean, default=False)  # 是否靠窗
    computer_available = db.Column(db.Boolean, default=False)  # 是否配备电脑
    description = db.Column(db.Text)
    position = db.Column(db.String(100))  # 位置描述
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    bookings = db.relationship('Booking', backref='seat', lazy='dynamic')

    @property
    def is_available_now(self):
        """检查座位当前是否可用"""
        from datetime import datetime
        now = datetime.utcnow()
        active_booking = self.bookings.filter(
            Booking.status == 'active',
            Booking.start_time <= now,
            Booking.end_time >= now
        ).first()
        return active_booking is None

    def __repr__(self):
        return f'<Seat {self.seat_number} in Room {self.room_id}>'

class TimeSlot(db.Model):
    __tablename__ = 'time_slots'

    id = db.Column(db.Integer, primary_key=True)
    slot_name = db.Column(db.String(50), nullable=False)  # 时段名称
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    max_booking_hours = db.Column(db.Integer, default=4)  # 最大预约时长(小时)
    is_active = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<TimeSlot {self.slot_name} {self.start_time}-{self.end_time}>'

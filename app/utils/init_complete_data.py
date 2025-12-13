"""
完整数据初始化脚本
确保系统启动时所有必要的表都有正确的数据
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from datetime import datetime, time

from app import db


def init_time_slots():
    """初始化时间段"""
    from app.models import TimeSlot

    if TimeSlot.query.count() == 0:
        time_slots = [
            TimeSlot(
                slot_name="上午时段",
                start_time=time(8, 0),
                end_time=time(12, 0),
                max_booking_hours=4,
                description="上午学习时段 8:00-12:00"
            ),
            TimeSlot(
                slot_name="下午时段",
                start_time=time(14, 0),
                end_time=time(18, 0),
                max_booking_hours=4,
                description="下午学习时段 14:00-18:00"
            ),
            TimeSlot(
                slot_name="晚上时段",
                start_time=time(19, 0),
                end_time=time(22, 0),
                max_booking_hours=3,
                description="晚上学习时段 19:00-22:00"
            ),
            TimeSlot(
                slot_name="全天时段",
                start_time=time(8, 0),
                end_time=time(22, 0),
                max_booking_hours=4,
                description="全天学习时段 8:00-22:00"
            )
        ]

        for slot in time_slots:
            db.session.add(slot)

        print("时间段已初始化")


def init_announcements():
    """初始化公告"""
    from app.models import Announcement

    if Announcement.query.count() == 0:
        announcements = [
            Announcement(
                title="欢迎使用自习室预约系统",
                content="欢迎使用校园自习室预约系统！请各位同学遵守预约规则，按时签到签退，共同维护良好的学习环境。",
                publisher_type="system",
                publish_date=datetime.now(),
                is_active=True,
                priority="high",
                target_audience="all"
            ),
            Announcement(
                title="预约系统使用须知",
                content="1. 每位同学同时只能有一个有效预约\n2. 最长可预约4小时\n3. 请在预约时间开始前30分钟内签到\n4. 如需取消预约，请在开始时间前2小时操作\n5. 三次未签到将影响预约权限",
                publisher_type="system",
                publish_date=datetime.now(),
                is_active=True,
                priority="normal",
                target_audience="students"
            ),
            Announcement(
                title="自习室开放时间调整通知",
                content="本学期自习室开放时间调整如下：\n- 图书馆一楼自习区：08:00-22:00\n- 图书馆二楼电子阅览室：09:00-21:00\n- 教学楼A栋自习室：07:30-22:30",
                publisher_type="system",
                publish_date=datetime.now(),
                is_active=True,
                priority="normal",
                target_audience="all"
            )
        ]

        for announcement in announcements:
            db.session.add(announcement)

        print("系统公告已初始化")


def init_missing_rooms():
    """初始化缺失的自习室"""
    from app.models import Seat, StudyRoom

    # 检查是否有教学楼A栋自习室
    teaching_building = StudyRoom.query.filter_by(room_number="TEA301").first()
    if not teaching_building:
        teaching_building = StudyRoom(
            room_number="TEA301",
            name="教学楼A栋自习室",
            building="教学楼A栋",
            floor="3楼",
            location="教学楼A栋3楼",
            description="教室环境，适合小组学习",
            capacity=40,  # 将在创建座位后更新
            open_time="07:30",
            close_time="22:30",
            room_type="discussion",
            has_power=True,
            has_wifi=True,
            has_air_conditioning=True,
            is_quiet=False,
            status="open"
        )
        db.session.add(teaching_building)
        db.session.flush()  # 获取ID

        # 为新房间创建座位
        for row in range(1, 9):  # 8行
            for col in range(1, 6):  # 5列
                seat_number = f"{chr(64+row)}{col}"  # A1, A2, B1, B2...

                # 不同类型座位
                if col == 1 or col == 5:  # 靠窗位置
                    seat_type = "window"
                elif col == 3:  # 中间位置，有电源
                    seat_type = "power"
                else:
                    seat_type = "standard"

                seat = Seat(
                    room_id=teaching_building.id,
                    seat_number=seat_number,
                    type=seat_type,
                    description=f"{seat_type}座位" if seat_type != "standard" else "标准座位",
                    position=f"第{row}行第{col}列",
                    power_socket=(seat_type == "power"),
                    window_seat=(seat_type == "window")
                )
                db.session.add(seat)

        teaching_building.capacity = 40  # 更新为实际座位数
        print("教学楼A栋自习室及座位已创建")


def init_complete_data():
    """完整数据初始化"""
    print("开始完整数据初始化...")

    try:
        # 初始化时间段
        init_time_slots()

        # 初始化公告
        init_announcements()

        # 检查并创建缺失的自习室
        init_missing_rooms()

        db.session.commit()
        print("\n完整数据初始化成功！")

        # 显示初始化结果
        from app.models import Announcement, Seat, StudyRoom, TimeSlot

        print("\n初始化结果统计:")
        print(f"时间段数量: {TimeSlot.query.count()}")
        print(f"公告数量: {Announcement.query.count()}")
        print(f"自习室数量: {StudyRoom.query.count()}")
        print(f"座位总数: {Seat.query.count()}")

    except Exception as e:
        db.session.rollback()
        print(f"数据初始化失败: {e}")
        raise


if __name__ == '__main__':
    from app import create_app

    app = create_app()
    with app.app_context():
        init_complete_data()

from app import create_app, db
from app.models import Admin, Seat, Student, StudyRoom


def init_database():
    """初始化数据库数据"""
    app = create_app()

    with app.app_context():
        # 创建所有表
        db.create_all()
        print("数据库表已创建")

        # 创建测试自习室
        if StudyRoom.query.count() == 0:
            rooms = [
                StudyRoom(
                    room_number="LIB101",
                    name="图书馆一楼自习区",
                    building="图书馆",
                    floor="1楼",
                    location="图书馆1楼东侧",
                    description="安静的学习环境，配备电源插座",
                    capacity=50,
                    open_time="08:00",
                    close_time="22:00"
                ),
                StudyRoom(
                    room_number="LIB201",
                    name="图书馆二楼电子阅览室",
                    building="图书馆",
                    floor="2楼",
                    location="图书馆2楼",
                    description="配备电脑，支持网络学习",
                    capacity=30,
                    open_time="09:00",
                    close_time="21:00"
                ),
                StudyRoom(
                    room_number="TEA301",
                    name="教学楼A栋自习室",
                    building="教学楼A栋",
                    floor="3楼",
                    location="教学楼A栋3楼",
                    description="教室环境，适合小组学习",
                    capacity=40,
                    open_time="07:30",
                    close_time="22:30"
                )
            ]

            for room in rooms:
                db.session.add(room)

            db.session.commit()
            print("测试自习室已创建")

            # 为每个自习室创建座位
            for room in StudyRoom.query.all():
                # 创建5x8的座位布局（共40个座位）
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
                            room_id=room.id,
                            seat_number=seat_number,
                            type=seat_type,
                            description=f"{seat_type}座位" if seat_type != "standard" else "标准座位",
                            position=f"第{row}行第{col}列",
                            power_socket=(seat_type == "power"),
                            window_seat=(seat_type == "window")
                        )
                        db.session.add(seat)

            db.session.commit()
            print("测试座位已创建")

        # 创建管理员用户
        if Admin.query.filter_by(username='admin').first() is None:
            admin = Admin(
                username='admin',
                email='admin@study-room.com',
                name='系统管理员',
                phone='13800138000'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("管理员用户已创建")

        # 创建测试学生用户
        if Student.query.filter_by(student_id='20210001').first() is None:
            test_students = [
                Student(
                    student_id='20210001',
                    email='student1@study-room.com',
                    name='张三',
                    phone='13800138001',
                    credit_score=100,
                    major='计算机科学与技术',
                    grade='2021级',
                    class_name='计科1班'
                ),
                Student(
                    student_id='20210002',
                    email='student2@study-room.com',
                    name='李四',
                    phone='13800138002',
                    credit_score=95,
                    major='软件工程',
                    grade='2021级',
                    class_name='软工2班'
                ),
                Student(
                    student_id='20210003',
                    email='student3@study-room.com',
                    name='王五',
                    phone='13800138003',
                    credit_score=88,
                    major='数据科学',
                    grade='2021级',
                    class_name='数据1班'
                )
            ]

            # 设置密码为123456
            for student in test_students:
                student.set_password('123456')
                db.session.add(student)

            db.session.commit()
            print("测试学生用户已创建")

        print("数据初始化完成！")
        print("\n管理员账号:")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n学生账号:")
        print("  张三 (学号: 20210001)")
        print("  李四 (学号: 20210002)")
        print("  王五 (学号: 20210003)")
        print("  学生账号密码统一为: 123456")

if __name__ == '__main__':
    init_database()

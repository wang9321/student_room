from app import create_app, db
from app.models import (
    Admin,
    Announcement,
    Booking,
    Seat,
    Student,
    StudyRoom,
    TimeSlot,
    User,
)
from app.utils.init_complete_data import init_complete_data

# 创建应用实例
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """为Flask shell提供上下文"""
    return {
        'db': db,
        'Student': Student,
        'Admin': Admin,
        'User': User,
        'StudyRoom': StudyRoom,
        'Seat': Seat,
        'Booking': Booking,
        'Announcement': Announcement,
        'TimeSlot': TimeSlot
    }

if __name__ == "__main__":
    with app.app_context():
        # 创建数据库表
        db.create_all()
        print("数据库表已创建")

        # 初始化完整数据（如果需要）
        init_complete_data()
        print("数据完整性检查完成")

    # 运行应用
    app.run(debug=True, host='0.0.0.0', port=5000)

# 导入所有模型
from .admin import Admin
from .booking import Announcement, Booking
from .student import Student
from .study_room import Seat, StudyRoom, TimeSlot
from .user import User

__all__ = ['Admin', 'Announcement', 'Booking', 'Seat', 'Student', 'StudyRoom', 'TimeSlot', 'User']

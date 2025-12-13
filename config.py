import os
from datetime import timedelta, timezone, datetime


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///study_room.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 预约时间设置
    MAX_BOOKING_HOURS = 4  # 最大预约小时数
    MAX_ADVANCE_DAYS = 7   # 最多提前预约天数
    AUTO_CANCEL_MINUTES = 15  # 超时未签到自动取消时间(分钟)

    # 会话设置
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    # 时区设置 (东八区，北京时间)
    TIMEZONE = timezone(timedelta(hours=8))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

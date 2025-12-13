from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Regexp,
    ValidationError,
)
from flask_wtf.csrf import CSRFProtect

from app.models import Student


class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名或学号', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    """注册表单"""
    # 移除 username 字段，因为 Student 模型不需要
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    student_id = StringField('学号', validators=[
        DataRequired(),
        Length(8, 20),
        Regexp('^[0-9]{8,20}$', 0, '学号必须为8-20位数字')
    ])
    full_name = StringField('真实姓名', validators=[DataRequired(), Length(2, 64)])
    phone = StringField('手机号', validators=[
        Length(0, 20),
        Regexp(r'^1[3-9]\d{9}$|^$', 0, '请输入有效的11位手机号码或留空')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(),
        Length(6, 128, message='密码长度至少6位')
    ])
    password2 = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password', message='两次输入的密码不一致')
    ])
    submit = SubmitField('注册')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('meta', {'csrf': False})
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def validate_email(self, field):
        if Student.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_student_id(self, field):
        if Student.query.filter_by(student_id=field.data).first():
            raise ValidationError('学号已被注册')

    def validate_phone(self, field):
        # 手机号验证已在正则表达式中处理，这里可以移除冗余验证
        pass


class ForgotPasswordForm(FlaskForm):
    """忘记密码表单"""
    email = StringField('邮箱地址', validators=[DataRequired(), Email(message='请输入有效的邮箱地址')])
    user_type = SelectField('用户类型',
                           choices=[('student', '学生'), ('admin', '管理员')],
                           validators=[DataRequired()])
    submit = SubmitField('发送重置链接')

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('meta', {'csrf': False})
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

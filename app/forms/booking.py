
from flask_wtf import FlaskForm
from wtforms import DateTimeField, HiddenField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError


class BookingForm(FlaskForm):
    """预约表单"""
    seat_id = HiddenField('座位ID', validators=[DataRequired()])
    start_time = DateTimeField('开始时间', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    end_time = DateTimeField('结束时间', validators=[DataRequired()], format='%Y-%m-%d %H:%M')
    purpose = TextAreaField('预约目的', validators=[Length(0, 200)])
    submit = SubmitField('确认预约')

    def validate_end_time(self, field):
        if field.data <= self.start_time.data:
            raise ValidationError('结束时间必须晚于开始时间')

        # 检查预约时长不超过最大限制
        duration = field.data - self.start_time.data
        if duration.total_seconds() / 3600 > 4:  # 最多4小时
            raise ValidationError('预约时长不能超过4小时')

class SelectRoomForm(FlaskForm):
    """选择自习室表单"""
    room_id = SelectField('选择自习室', coerce=int, validators=[DataRequired()])
    submit = SubmitField('下一步：选择座位')

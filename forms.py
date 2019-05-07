from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, RadioField, DateField
from wtforms.validators import DataRequired, Length, EqualTo


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class LoginForm(MyBaseForm):
    username = StringField('用户名', validators=[DataRequired()], render_kw={'placeholder': '用户名'})
    password = PasswordField('密码', validators=[DataRequired()], render_kw={'placeholder': '密码'})
    submit = SubmitField('登录')


class PersonalForm(MyBaseForm):
    username = StringField('用户名', validators=[DataRequired()], render_kw={'placeholder': '用户名'})
    name = StringField('姓名', validators=[DataRequired()], render_kw={'placeholder': '姓名'})
    birthday = DateField('生日', validators=[DataRequired(message='日期格式不正确')], render_kw={'placeholder': '生日'})
    sex = RadioField('性别', choices=(('男', '男'), ('女', '女')), default='男')
    submit = SubmitField('修改信息')


class UpdatePasswordForm(MyBaseForm):
    oldPassword = PasswordField('旧密码', validators=[DataRequired(), Length(3, 100)], render_kw={'placeholder': '旧密码'})
    newPassword1 = PasswordField('新密码', validators=[DataRequired(), Length(3, 100)], render_kw={'placeholder': '新密码'})
    newPassword2 = PasswordField('确认密码', validators=[DataRequired(), Length(3, 100), EqualTo('newPassword1', '新密码填入不一致')
                                                     ], render_kw={'placeholder': '确认密码'})
    submit = SubmitField('修改密码')

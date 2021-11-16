from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, InputRequired

class RegistrForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Почта', validators=[Email()])
    password = PasswordField('Пароль', validators=[InputRequired()])
    remember_me = BooleanField('Запомни меня', default = False)
    submit = SubmitField('Войти/Зарегистрироваться')

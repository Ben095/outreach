from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.recaptcha import RecaptchaField


class QueryGoogle(Form):
    QueryGoogle = TextField('query',
        validators=[DataRequired()])


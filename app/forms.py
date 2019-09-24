from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class EditUps(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    api_key = StringField('API Key', validators=[DataRequired()])
    ship_num = StringField('Shipper Number', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditFedex(FlaskForm):
    password = StringField('Password', validators=[DataRequired()])
    api_key = StringField('API Key', validators=[DataRequired()])
    ship_num = StringField('Shipper Number', validators=[DataRequired()])
    meter_num = StringField('Meter Number', validators=[DataRequired()])
    submit = SubmitField('Submit')
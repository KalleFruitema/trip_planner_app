from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    
class TimespanSelectionForm(FlaskForm):
    start_date = DateField('start_date', format='%d-%m-%Y')
    end_date = DateField('end_date', format='%d-%m-%Y')
    submit = SubmitField('Submit')
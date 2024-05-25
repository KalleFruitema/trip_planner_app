from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, StringField, PasswordField, SelectField
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
    

class JoinPlanForm(FlaskForm):
    plan_code = StringField('Plan Code')
    submit = SubmitField('Submit')
    

class CreatePlanForm(FlaskForm):
    name = StringField('Plan name', validators=[DataRequired()])
    description = StringField('Plan description (optional)')
    start_date = DateField('Start date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create plan')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange


# Forms for Registration
class CustomerRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Please enter the same password again')])
    building_number = StringField('Building Number', validators=[DataRequired(), Length(min=1, max=30)])
    street = StringField('Street', validators=[DataRequired(), Length(min=1, max=30)])
    city = StringField('City', validators=[DataRequired(), Length(min=1, max=30)])
    state = StringField('State', validators=[DataRequired(), Length(min=1, max=30)])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    passport_number = StringField('Passport Number', validators=[DataRequired(), Length(min=1, max=30)])
    passport_expiration = DateField('Passport Expiration', validators=[DataRequired()])
    passport_country = StringField('Passport Country', validators=[DataRequired(), Length(min=1, max=50)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])

    submit = SubmitField('Customer Sign Up')


class StaffRegistrationForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Please type your password again')])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    airline_name = StringField('Airline Name', validators=[DataRequired(), Length(min=1, max=50)])

    submit = SubmitField('Staff Sign Up')


class BookingAgentRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Please type your password again')])
    booking_agent_id = IntegerField('Booking Agent ID', validators=[DataRequired(), Length(min=11, max=11)])

    submit = SubmitField('Booking Agent Sign Up')


# Forms for Login
class CustomerLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
    # remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class BookingAgentLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
    # remember = BooleanField('Remember Me')

    submit = SubmitField('Login')


class StaffLoginForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
    # remember = BooleanField('Remember Me')

    submit = SubmitField('Login')
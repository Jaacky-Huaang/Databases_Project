from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, DateTimeField, SelectField
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
    booking_agent_id = IntegerField('Booking Agent ID', validators=[DataRequired()])  # how to set length to be 11?

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


class PublicSearchUpcomingFlightForm(FlaskForm):
    departure_place = StringField('Departure Airport/City', validators=[])
    arrival_place = StringField('Arrival Airport/City', validators=[])

    # Maybe DateTimeField?
    departure_time = StringField('Departure Time', validators=[])
    arrival_time = StringField('Arrival Time', validators=[])

    submit = SubmitField('Search')


class PublicSearchFlightStatusForm(FlaskForm):
    flight_number = IntegerField('Flight Number', validators=[])
    departure_time = StringField('Departure Time', validators=[])
    arrival_time = StringField('Arrival Time', validators=[])

    submit = SubmitField('Search')

class CustomerSpendingForm(FlaskForm):
    start_date = DateField('Start Date', validators=[])
    end_date = DateField('End Date', validators=[])

    submit = SubmitField('Search')


class PurchaseCus(FlaskForm):
    # flight_number = IntegerField('Flight Number', validators=[DataRequired()])
    agent = StringField('Agent_ID', validators=[])
    # customer = StringField('Customer_Email', validators=[])
    submit = SubmitField('Purchase')


class PurchaseAgen(FlaskForm):
    # flight_number = IntegerField('Flight Number', validators=[DataRequired()])
    customer = StringField('Customer_Email', validators=[])
    # agent = StringField('Agent_ID', validators=[])
    submit = SubmitField('Purchase')

class CreateFlightForm(FlaskForm):
    # airline_name = StringField('Airline Name', validators=[DataRequired(), Length(min=1, max=50)])
    flight_num = IntegerField('Flight Number', validators=[DataRequired()])
    departure_airport = StringField('Departure Airport', validators=[DataRequired(), Length(min=1, max=50)])
    departure_time = DateTimeField('Departure Time', validators=[DataRequired()])
    arrival_airport = StringField('Arrival Airport', validators=[DataRequired(), Length(min=1, max=50)])
    arrival_time = DateTimeField('Arrival Time', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    status = SelectField('Status', choices=['upcoming', 'in_progress', 'delayed'])
    airplane_id = IntegerField('Airplane ID', validators=[DataRequired()])

    submit = SubmitField('Create')

class AddAirplaneForm(FlaskForm):
    identifier = StringField('Identifier')
    airplane_id = IntegerField('Airplane ID', validators=[DataRequired()])
    seats = IntegerField('Seats', validators=[DataRequired()])

    submit = SubmitField('Add')


class AddAirportForm(FlaskForm):
    identifier = StringField('Identifier')
    airport_name = StringField('Airport Name', validators=[DataRequired(), Length(min=1, max=50)])
    airport_city = StringField('Airport City', validators=[DataRequired(), Length(min=1, max=50)])

    submit = SubmitField('Add')


class AirlineStaffSearchForm(FlaskForm):
    identifier = StringField('Identifier')
    start_time = DateField('Start Time', validators=[])
    end_time = DateField('End Time', validators=[])
    departure_place = StringField('Departure Airport/City', validators=[])
    arrival_place = StringField('Arrival Airport/City', validators=[])

    submit = SubmitField('Search Flight')


class ChangeFlightStatusForm(FlaskForm):
    identifier = StringField('Identifier')
    flight_num = IntegerField('Flight Number', validators=[DataRequired()])
    status = SelectField('New Status', choices=['', 'upcoming', 'in_progress', 'delayed'])

    submit = SubmitField('Submit Change')


class ViewTicketReportsForm(FlaskForm):
    identifier = StringField('Identifier')
    start_date = DateField('Start Date', validators=[])
    end_date = DateField('End Date', validators=[])

    submit = SubmitField('View Reports')

class GrantNewPermissionForm(FlaskForm):
    identifier = StringField('Identifier')
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
    permission = SelectField('Permission', choices=['Operator', 'Admin'])

    submit = SubmitField('Grant Permission')

class AddBookingAgentToAirlineForm(FlaskForm):
    identifier = StringField('Identifier')
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])

    submit = SubmitField('Add Booking Agent to Airline')
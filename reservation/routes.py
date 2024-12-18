from flask import render_template, request, url_for, redirect, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from reservation import app, conn, bcrypt
import reservation.forms as forms
import json
import datetime
from dateutil.relativedelta import relativedelta

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    # public search
    active_tab = request.form.get('active_tab', '#upcoming-flights')
    form_upcoming_flight = forms.PublicSearchUpcomingFlightForm()
    if form_upcoming_flight.validate_on_submit():
        departure_place = form_upcoming_flight.departure_place.data
        arrival_place = form_upcoming_flight.arrival_place.data
        departure_time = form_upcoming_flight.departure_time.data
        arrival_time = form_upcoming_flight.arrival_time.data

        cursor = conn.cursor()
        query_upcoming_flight = f'SELECT * FROM flight F LEFT JOIN airport A1 ON F.departure_airport = A1.airport_name LEFT JOIN airport A2 ON F.arrival_airport = A2.airport_name NATURAL JOIN airplane P WHERE (A1.airport_name LIKE "%{departure_place}%" OR A1.airport_city LIKE "%{departure_place}%") AND (A2.airport_name LIKE "%{arrival_place}%" OR A2.airport_city LIKE "%{arrival_place}%") AND F.departure_time LIKE "%{departure_time}%" AND F.arrival_time LIKE "%{arrival_time}%" AND F.status = "upcoming"'
        cursor.execute(query_upcoming_flight)
        search_result = cursor.fetchall()
        cursor.close()
        if len(search_result) != 0:
            return redirect(url_for('upcoming_flight', search_result=json.dumps(search_result, default=str)))

    form_flight_status = forms.PublicSearchFlightStatusForm()
    flight_number = '' if form_flight_status.flight_number.data==None else form_flight_status.flight_number.data
    departure_time = '' if form_flight_status.departure_time.data==None else form_flight_status.departure_time.data
    arrival_time = '' if form_flight_status.arrival_time.data==None else form_flight_status.arrival_time.data
    cursor = conn.cursor()
    print(flight_number, departure_time, arrival_time)
    query_flight_status = f'SELECT * FROM flight WHERE flight_num LIKE "%{flight_number}%" AND departure_time LIKE "%{departure_time}%" AND arrival_time LIKE "%{arrival_time}%"'
    cursor.execute(query_flight_status)
    status_search_result = cursor.fetchall()
    cursor.close()

    return render_template('index.html', active_tab=active_tab,
                           form_upcoming_flight=form_upcoming_flight, form_flight_status=form_flight_status, status_search_result=status_search_result)
# @app.route('/', methods=['GET', 'POST'])
# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     # public search
#     class PublicSearchUpcomingFlightForm(FlaskForm):
#         departure_place = StringField('Departure Airport/City', validators=[])
#         arrival_place = StringField('Arrival Airport/City', validators=[])

#         # Maybe DateTimeField?
#         departure_time = StringField('Departure Time', validators=[])
#         arrival_time = StringField('Arrival Time', validators=[])
#         submit = SubmitField('Search')
    
#     form_upcoming_flight = PublicSearchUpcomingFlightForm()
#     if form_upcoming_flight.validate_on_submit():
#         departure_place = form_upcoming_flight.departure_place.data
#         arrival_place = form_upcoming_flight.arrival_place.data
#         departure_time = form_upcoming_flight.departure_time.data
#         arrival_time = form_upcoming_flight.arrival_time.data

#         cursor = conn.cursor()
#         query_upcoming_flight = f'SELECT * FROM flight F LEFT JOIN airport A1 ON F.departure_airport = A1.airport_name LEFT JOIN airport A2 ON F.arrival_airport = A2.airport_name NATURAL JOIN airplane P WHERE (A1.airport_name LIKE "%{departure_place}%" OR A1.airport_city LIKE "%{departure_place}%") AND (A2.airport_name LIKE "%{arrival_place}%" OR A2.airport_city LIKE "%{arrival_place}%") AND F.departure_time LIKE "%{departure_time}%" AND F.arrival_time LIKE "%{arrival_time}%" AND F.status = "upcoming"'
#         cursor.execute(query_upcoming_flight)
#         search_result = cursor.fetchall()
#         cursor.close()
#         if len(search_result) == 0:
#             flash('No flight found', 'danger')
#         else:
#             return redirect(url_for('upcoming_flight', search_result=json.dumps(search_result, default=str)))

#     class PublicSearchFlightStatusForm(FlaskForm):
#         flight_number = IntegerField('Flight Number', validators=[])
#         departure_time = StringField('Departure Time', validators=[])
#         arrival_time = StringField('Arrival Time', validators=[])
#         submit = SubmitField('Search')
    
#     form_flight_status = PublicSearchFlightStatusForm()
#     flight_number = '' if form_flight_status.flight_number.data==None else form_flight_status.flight_number.data
#     departure_time = '' if form_flight_status.departure_time.data==None else form_flight_status.departure_time.data
#     arrival_time = '' if form_flight_status.arrival_time.data==None else form_flight_status.arrival_time.data
#     cursor = conn.cursor()
#     query_flight_status = f'SELECT * FROM flight WHERE flight_num LIKE "%{flight_number}%" AND departure_time LIKE "%{departure_time}%" AND arrival_time LIKE "%{arrival_time}%"'
#     cursor.execute(query_flight_status)
#     status_search_result = cursor.fetchall()
#     cursor.close()

#     return render_template('index.html', form_upcoming_flight=form_upcoming_flight, form_flight_status=form_flight_status, status_search_result=status_search_result)


# Define route for searching upcoming flight
@app.route('/upcoming_flight/<search_result>', methods=['GET', 'POST'])
def upcoming_flight(search_result):
    if 'status' not in session:
        status = 'public'
    else:
        if session['status'] == 'customer':
            status = 'customer'
        elif session['status'] == 'agent':
            status = 'agent'
        else:
            status = 'staff'
    search_result = json.loads(search_result)
    return render_template('upcoming_flight.html', search_result=search_result,status = status)



# Define route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

# customer registration
@app.route('/customer_registration', methods=['GET', 'POST'])
def register_customer():
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

    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        building_number = form.building_number.data
        street = form.street.data
        city = form.city.data
        state = form.state.data
        phone_number = form.phone_number.data
        passport_number = form.passport_number.data
        passport_expiration = form.passport_expiration.data
        passport_country = form.passport_country.data
        date_of_birth = form.date_of_birth.data

        cursor = conn.cursor()
        query_find_email = "SELECT email FROM customer WHERE email = '{}'"
        cursor.execute(query_find_email.format(email))
        dup_emails = cursor.fetchall()
        print(dup_emails)
        if len(dup_emails) > 0:
            flash('Email already exists!', 'danger')
            # return redirect(url_for('register'))
            cursor.close()
        else:
            query = "INSERT INTO customer VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
            cursor.execute(query.format(email, name, hashed_password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
            conn.commit()
            flash(f'Account created for {form.name.data}!', 'success')
            cursor.close()

            return redirect(url_for('login_customer'))

    return render_template('register_customer.html', title='Register as Customer', form=form)

# define route for agent registration
@app.route('/agent_registration', methods=['GET', 'POST'])
def register_agent():

    class BookingAgentRegistrationForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Please type your password again')])
        booking_agent_id = IntegerField('Booking Agent ID', validators=[DataRequired()])  # how to set length to be 11?
        submit = SubmitField('Booking Agent Sign Up')

    form = BookingAgentRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        booking_agent_id = form.booking_agent_id.data

        cursor = conn.cursor()
        # check for duplicate
        query_find_email = "SELECT email FROM booking_agent WHERE email = '{}'"
        cursor.execute(query_find_email.format(email))
        dup_emails = cursor.fetchall()
        query_find_agent_id = "SELECT booking_agent_id FROM booking_agent WHERE booking_agent_id = '{}'"
        cursor.execute(query_find_agent_id.format(booking_agent_id))
        dup_agent_ids = cursor.fetchall()
        if len(dup_emails) + len(dup_agent_ids) > 0:
            if len(dup_emails) > 0:
                flash('Email already exists!', 'danger')
                cursor.close()
            if len(dup_agent_ids) > 0:
                flash('Agent ID already exists!', 'danger')
                cursor.close()
        else:
            query = "INSERT INTO booking_agent VALUES ('{}', '{}', '{}')"
            cursor.execute(query.format(email, hashed_password, booking_agent_id))
            conn.commit()
            flash(f'Account created for {form.email.data}!', 'success')
            cursor.close()

            return redirect(url_for('login_agent'))

    return render_template('register_agent.html', title='Register as Agent', form=form)

# define route for airline staff registration
@app.route('/staff_registration', methods=['GET', 'POST'])
def register_airline_staff():
    class StaffRegistrationForm(FlaskForm):
        user_name = StringField('User Name', validators=[DataRequired(), Length(min=1, max=50)])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Please type your password again')])
        first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
        last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
        date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
        airline_name = StringField('Airline Name', validators=[DataRequired(), Length(min=1, max=50)])
        submit = SubmitField('Staff Sign Up')

    form = StaffRegistrationForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        first_name = form.first_name.data
        last_name = form.last_name.data
        date_of_birth = form.date_of_birth.data
        airline_name = form.airline_name.data

        cursor = conn.cursor()
        query_find_user_name = "SELECT username FROM airline_staff WHERE username = '{}'"
        cursor.execute(query_find_user_name.format(user_name))
        dup_user_names = cursor.fetchall()
        if len(dup_user_names) > 0:
            flash('User name already exists!', 'danger')
            cursor.close()
        else:
            query = "INSERT INTO airline_staff VALUES ('{}', '{}', '{}', '{}', '{}', '{}')"
            cursor.execute(query.format(user_name, hashed_password, first_name, last_name, date_of_birth, airline_name))
            conn.commit()
            flash(f'Account created for {form.user_name.data}!', 'success')
            cursor.close()

            return redirect(url_for('login_airline_staff'))

    return render_template('register_airline_staff.html', title='Register as Airline Staff', form=form)

# define route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

# define route for customer login
@app.route('/login_customer', methods=['GET', 'POST'])
def login_customer():

    class CustomerLoginForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
        submit = SubmitField('Login')
    
    form = CustomerLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = conn.cursor()
        query = "SELECT * FROM customer WHERE email = '{}'"
        cursor.execute(query.format(email))
        data = cursor.fetchone()
        cursor.close()

        if data and bcrypt.check_password_hash(data['password'], password):
            # add the customer email to the session
            session['email'] = email
            # add the user status to the session
            session['status'] = 'customer'
            flash(f'You have successfully logged in as {email}!', 'success')

            return redirect(url_for('home'))  # Change later
        elif not data:  # handle the case when the email does not exist
            flash('Email does not exist!', 'danger')
        else:  # handle the case when the password is wrong
            flash('Wrong password. Please enter the password again.', 'danger')

    return render_template('login_customer.html', title='Login as Customer', form=form)

# define route for agent login
@app.route('/login_agent', methods=['GET', 'POST'])
def login_agent():
    
    class BookingAgentLoginForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
        submit = SubmitField('Login')
    
    form = BookingAgentLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = conn.cursor()
        query = "SELECT * FROM booking_agent WHERE email = '{}'"
        cursor.execute(query.format(email))
        data = cursor.fetchone()
        cursor.close()

        if data and bcrypt.check_password_hash(data['password'], password):
            # add the agent email to the session
            session['email'] = email
            # add the user status to the session
            session['status'] = 'agent'
            session['agent_id'] = data['booking_agent_id']
            flash(f'You have successfully logged in as {email}!', 'success')

            return redirect(url_for('home'))  # Change later
        elif not data:  # handle the case when the email does not exist
            flash('Email does not exist!', 'danger')
        else:  # handle the case when the password is wrong
            flash('Wrong password. Please enter the password again.', 'danger')

    return render_template('login_agent.html', title='Login as Agent', form=form)

# define route for airline staff login
@app.route('/login_staff', methods=['GET', 'POST'])
def login_airline_staff():
    class StaffLoginForm(FlaskForm):
        user_name = StringField('User Name', validators=[DataRequired(), Length(min=1, max=50)])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=50)])
        submit = SubmitField('Login')

    form = StaffLoginForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data

        cursor = conn.cursor()
        query = "SELECT * FROM airline_staff WHERE username = '{}'"
        cursor.execute(query.format(user_name))
        data = cursor.fetchone()
        cursor.close()

        if data and bcrypt.check_password_hash(data['password'], password):
            flash(f'You have successfully logged in as {user_name}!', 'success')
            # add the staff username to the session
            session['user_name'] = user_name
            # add the user status to the session
            session['status'] = 'airline_staff'

            # add the permission type and airline of the staff
            cursor = conn.cursor()
            query = "SELECT permission_type FROM permission WHERE username = '{}'"
            cursor.execute(query.format(user_name))
            permission = cursor.fetchall()

            query = "SELECT airline_name FROM airline_staff WHERE username = '{}'"
            cursor.execute(query.format(user_name))
            airline = cursor.fetchone()
            cursor.close()

            if 'permission_type' not in session:
                session['permission_type'] = []
            for p in permission:
                session['permission_type'].append(p['permission_type'])

            session['airline'] = airline['airline_name']

            return redirect(url_for('home'))  # also change here later

        elif not data:  # handle the case when the email does not exist
            flash('Username does not exist!', 'danger')
        else:  # handle the case when the password is wrong
            flash('Wrong password. Please enter the password again.', 'danger')

    return render_template('login_airline_staff.html', title='Login as Airline Staff', form=form)

# define route for logout
@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('user_name', None)
    session.pop('status', None)
    session.pop('agent_id', None)
    session.pop('airline', None)
    session.pop('permission_type', None)
    flash('You have successfully logged out!', 'info')
    return redirect(url_for('home'))


@app.route('/dashboard_customer', methods=['GET', 'POST'])
def dashboard_customer():

    class CustomerSpendingForm(FlaskForm):
        start_date = DateField('Start Date', validators=[])
        end_date = DateField('End Date', validators=[])
        submit = SubmitField('Search')

    # display purchased flight info
    cursor = conn.cursor()
    query = f"SELECT * FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE customer_email = '{session['email']}'"
    cursor.execute(query)
    purchased_flights = cursor.fetchall()
    cursor.close()

    # track customer spending
    form_customer_spending = CustomerSpendingForm()
    start_date = datetime.date.today() - relativedelta(years=1) if form_customer_spending.start_date.data==None else form_customer_spending.start_date.data
    end_date = datetime.date.today() if form_customer_spending.end_date.data==None else form_customer_spending.end_date.data

    cursor = conn.cursor()
    query = f"SELECT YEAR(purchase_date) as year, MONTH(purchase_date) as month, SUM(price) AS total_spending FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE customer_email = '{session['email']}' AND purchase_date BETWEEN '{start_date}' AND '{end_date}' GROUP BY year, month"
    cursor.execute(query)
    customer_spending = cursor.fetchall()
    cursor.close()

    spending_date_dic = {}
    for row in customer_spending:
        spending_date_dic[str(row['year']) + '-' + str(row['month'])] = float(row['total_spending'])

    date_list = []
    spending_list = []
    while start_date <= end_date:
        date_list.append(str(start_date.year) + '-' + str(start_date.month))
        if str(start_date.year) + '-' + str(start_date.month) in spending_date_dic:
            spending_list.append(spending_date_dic[str(start_date.year) + '-' + str(start_date.month)])
        else:
            spending_list.append(0)
        start_date += relativedelta(months=1)

    return render_template('dashboard_customer.html', purchased_flights=purchased_flights, form_customer_spending=form_customer_spending, date_list=json.dumps(date_list), spending_list=json.dumps(spending_list))


@app.route('/dashboard_agent', methods=['GET', 'POST'])
def dashboard_agent():
    class CustomerSpendingForm(FlaskForm):
        start_date = DateField('Start Date', validators=[])
        end_date = DateField('End Date', validators=[])
        submit = SubmitField('Search')

    # display purchased flight info
    cursor = conn.cursor()
    query = f"SELECT * FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']}'"
    cursor.execute(query)
    purchased_flights = cursor.fetchall()
    cursor.close()

    # track customer spending
    form_customer_spending = CustomerSpendingForm()
    start_date = datetime.date.today() - relativedelta(years=1) if form_customer_spending.start_date.data==None else form_customer_spending.start_date.data
    end_date = datetime.date.today() if form_customer_spending.end_date.data==None else form_customer_spending.end_date.data

    cursor = conn.cursor()
    query = f"SELECT YEAR(purchase_date) as year, MONTH(purchase_date) as month, SUM(price) * 0.1 AS total_spending FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']}' AND purchase_date BETWEEN '{start_date}' AND '{end_date}' GROUP BY year, month"
    cursor.execute(query)
    customer_spending = cursor.fetchall()
    cursor.close()


    spending_date_dic = {}
    for row in customer_spending:
        spending_date_dic[str(row['year']) + '-' + str(row['month'])] = float(row['total_spending'])

    date_list = []
    spending_list = []
    while start_date <= end_date:
        date_list.append(str(start_date.year) + '-'  + str(start_date.month))
        if str(start_date.year) + '-' + str(start_date.month) in spending_date_dic:
            spending_list.append(spending_date_dic[str(start_date.year) + '-' + str(start_date.month)])
        else:
            spending_list.append(0)
        start_date += relativedelta(months=1)

    return render_template('dashboard_agent.html', purchased_flights=purchased_flights, form_customer_spending=form_customer_spending, date_list=json.dumps(date_list), spending_list=json.dumps(spending_list))



@app.route('/dashboard_staff', methods=['GET', 'POST'])
def dashboard_airline_staff():
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
    class GrantNewPermissionForm(FlaskForm):
        identifier = StringField('Identifier')
        email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
        permission = SelectField('Permission', choices=['Operator', 'Admin'])
        submit = SubmitField('Grant Permission')

    class AddBookingAgentToAirlineForm(FlaskForm):
        identifier = StringField('Identifier')
        email = StringField('Email', validators=[DataRequired(), Email(), Length(min=1, max=50)])
        submit = SubmitField('Add Booking Agent to Airline')
    class ChangeFlightStatusForm(FlaskForm):
        identifier = StringField('Identifier')
        flight_num = IntegerField('Flight Number', validators=[DataRequired()])
        status = SelectField('New Status', choices=['', 'upcoming', 'in_progress', 'delayed'])
        submit = SubmitField('Submit Change')
    
    class CreateFlightForm(FlaskForm):
        flight_num = IntegerField('Flight Number', validators=[DataRequired()])
        departure_airport = StringField('Departure Airport', validators=[DataRequired(), Length(min=1, max=50)])
        departure_time = DateTimeField('Departure Time', validators=[DataRequired()])
        arrival_airport = StringField('Arrival Airport', validators=[DataRequired(), Length(min=1, max=50)])
        arrival_time = DateTimeField('Arrival Time', validators=[DataRequired()])
        price = IntegerField('Price', validators=[DataRequired()])
        status = SelectField('Status', choices=['upcoming', 'in_progress', 'delayed'])
        airplane_id = IntegerField('Airplane ID', validators=[DataRequired()])
        submit = SubmitField('Create')
    
    airline_staff_search_form = AirlineStaffSearchForm()
    add_airplane_form = AddAirplaneForm()
    add_airport_form = AddAirportForm()
    change_flight_status_form = ChangeFlightStatusForm()
    grant_new_permission_form = GrantNewPermissionForm()
    add_booking_agent_to_airline_form = AddBookingAgentToAirlineForm()
    create_flight_form = CreateFlightForm()

    # handle the search flight form
    departure_place = '' if airline_staff_search_form.departure_place.data is None else airline_staff_search_form.departure_place.data
    arrival_place = '' if airline_staff_search_form.arrival_place.data is None else airline_staff_search_form.arrival_place.data
    start_time = datetime.date.today() if airline_staff_search_form.start_time.data is None else airline_staff_search_form.start_time.data
    end_time = (datetime.date.today() + relativedelta(days=30)) if airline_staff_search_form.end_time.data is None else airline_staff_search_form.end_time.data

    cursor = conn.cursor()
    query = (f"SELECT * FROM flight F "
             f"LEFT JOIN airport A1 ON F.departure_airport = A1.airport_name "
             f"LEFT JOIN airport A2 ON F.arrival_airport = A2.airport_name "
             f"WHERE F.airline_name = '{session['airline']}' "
             f"AND (F.departure_airport LIKE '%{departure_place}%' OR A1.airport_city LIKE '%{departure_place}%') "
             f"AND (F.arrival_airport LIKE '%{arrival_place}%' OR A2.airport_city LIKE '%{arrival_place}%') "
             f"AND (F.departure_time BETWEEN '{start_time}' AND '{end_time}' OR F.arrival_time BETWEEN '{start_time}' AND '{end_time}')")
    cursor.execute(query)
    flights = cursor.fetchall()
    cursor.close()

    # handle the add airplane form
    if add_airplane_form.identifier.data == 'add_airplane' and add_airplane_form.validate_on_submit():
        airplane_id = add_airplane_form.airplane_id.data
        seats = add_airplane_form.seats.data

        # check whether the airplane exists
        cursor = conn.cursor()
        query = "SELECT * FROM airplane WHERE airplane_id = '{}' AND airline_name = '{}'"
        cursor.execute(query.format(airplane_id, session['airline']))
        data = cursor.fetchone()
        print(data)
        cursor.close()
        if data:
            flash('The airplane already exists!', 'danger')
        else:
            # add the airplane to the database
            cursor = conn.cursor()
            query = "INSERT INTO airplane VALUES ('{}', '{}', '{}')"
            cursor.execute(query.format(session['airline'], airplane_id, seats))
            conn.commit()
            cursor.close()
            flash('You have successfully added a new airplane!', 'success')
            return redirect(url_for('dashboard_airline_staff'))

    # handle the add airport form
    if add_airport_form.identifier.data == 'add_airport' and add_airport_form.validate_on_submit():
        airport_name = add_airport_form.airport_name.data
        airport_city = add_airport_form.airport_city.data

        # check whether the airport exists
        cursor = conn.cursor()
        query = "SELECT * FROM airport WHERE airport_name = '{}'"
        cursor.execute(query.format(airport_name))
        data = cursor.fetchone()
        cursor.close()
        if data:
            flash('The airport already exists!', 'danger')
        else:
            # add the airport to the database
            cursor = conn.cursor()
            query = "INSERT INTO airport VALUES ('{}', '{}')"
            cursor.execute(query.format(airport_name, airport_city))
            conn.commit()
            cursor.close()
            flash('You have successfully added a new airport!', 'success')
            return redirect(url_for('dashboard_airline_staff'))

    # handle the change flight status form
    if change_flight_status_form.identifier.data == 'change_flight_status' and change_flight_status_form.validate_on_submit():
        flight_num = change_flight_status_form.flight_num.data
        status = change_flight_status_form.status.data

        if status not in ['upcoming', 'delayed', 'canceled']:
            flash('No new status is assigned!', 'danger')
            return redirect(url_for('dashboard_airline_staff'))
        # check whether the flight exists
        cursor = conn.cursor()
        query = "SELECT * FROM flight WHERE flight_num = '{}'"
        cursor.execute(query.format(flight_num))
        data = cursor.fetchone()
        cursor.close()
        if not data:
            flash('The flight does not exist!', 'danger')
        else:
            # change the status of the flight
            cursor = conn.cursor()
            query = "UPDATE flight SET status = '{}' WHERE flight_num = '{}'"
            cursor.execute(query.format(status, flight_num))
            conn.commit()
            cursor.close()
            flash('You have successfully changed the status of the flight!', 'success')
            return redirect(url_for('dashboard_airline_staff'))

    # handle the grant new permission form
    if grant_new_permission_form.identifier.data == 'grant_new_permission' and grant_new_permission_form.validate_on_submit():
        email = grant_new_permission_form.email.data
        permission_type = grant_new_permission_form.permission.data

        # check whether the email exists
        cursor = conn.cursor()
        query = "SELECT * FROM airline_staff WHERE username = '{}'"
        cursor.execute(query.format(email))
        data = cursor.fetchone()
        cursor.close()
        if not data:
            flash('The email does not exist!', 'danger')
            return redirect(url_for('dashboard_airline_staff'))
        else:
            # check whether the email has already been granted the permission
            cursor = conn.cursor()
            query = "SELECT * FROM permission WHERE username = '{}' AND permission_type = '{}'"
            cursor.execute(query.format(email, permission_type))
            data = cursor.fetchone()
            cursor.close()
            if data:
                flash('The email has already been granted the permission!', 'danger')
                return redirect(url_for('dashboard_airline_staff'))
            else:
                # grant the permission to the email
                cursor = conn.cursor()
                query = "INSERT INTO permission VALUES ('{}', '{}')"
                cursor.execute(query.format(email, permission_type))
                conn.commit()
                cursor.close()
                flash('You have successfully granted the permission!', 'success')
                return redirect(url_for('dashboard_airline_staff'))

    # handle the add booking agent to airline form
    if add_booking_agent_to_airline_form.identifier.data == 'add_booking_agent_to_airline' and add_booking_agent_to_airline_form.validate_on_submit():
        agent_email = add_booking_agent_to_airline_form.email.data

        # check whether the email of the booking agent exists
        cursor = conn.cursor()
        query = "SELECT * FROM booking_agent WHERE email = '{}'"
        cursor.execute(query.format(agent_email))
        data = cursor.fetchone()
        cursor.close()
        if not data:
            flash('The booking agent does not exist!', 'danger')
            return redirect(url_for('dashboard_airline_staff'))
        else:
            # check whether the agent is already working for the airline
            cursor = conn.cursor()
            query = "SELECT * FROM booking_agent_work_for WHERE email = '{}' AND airline_name = '{}'"
            cursor.execute(query.format(agent_email, session['airline']))
            data = cursor.fetchone()
            cursor.close()
            if data:
                flash(f"The booking agent has already been added to {session['airline']} airline!", 'danger')
                return redirect(url_for('dashboard_airline_staff'))
            else:
                # add the booking agent to the airline
                cursor = conn.cursor()
                query = "INSERT INTO booking_agent_work_for VALUES ('{}', '{}')"
                cursor.execute(query.format(agent_email, session['airline']))
                conn.commit()
                cursor.close()
                flash(f'You have successfully added booking agent {agent_email} to your airline!', 'success')
                return redirect(url_for('dashboard_airline_staff'))

    # handle the create flight form (merged from create_flight route)
    if create_flight_form.validate_on_submit():
        # Check user permissions
        if 'permission_type' not in session:
            flash('Please login as an airline staff first!', 'danger')
            return redirect(url_for('login'))
        elif 'Admin' not in session['permission_type']:
            flash('You are not admin, so you are not authorized :(', 'danger')
            return redirect(url_for('dashboard_airline_staff'))

        flight_num = create_flight_form.flight_num.data
        departure_airport = create_flight_form.departure_airport.data
        departure_time = create_flight_form.departure_time.data
        arrival_airport = create_flight_form.arrival_airport.data
        arrival_time = create_flight_form.arrival_time.data
        price = create_flight_form.price.data
        status = create_flight_form.status.data
        airplane_id = create_flight_form.airplane_id.data

        # check whether the flight already exists
        cursor = conn.cursor()
        query = "SELECT * FROM flight WHERE flight_num = '{}'"
        cursor.execute(query.format(flight_num))
        data = cursor.fetchone()
        cursor.close()
        if data:
            flash('The flight already exists!', 'danger')
        else:
            # add the flight to the database
            cursor = conn.cursor()
            query = ("INSERT INTO flight VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')")
            cursor.execute(query.format(session['airline'], flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id))
            conn.commit()
            cursor.close()

            # get the latest ticket_id
            cursor = conn.cursor()
            query = "SELECT MAX(ticket_id) as max_id FROM ticket"
            cursor.execute(query)
            latest_id = cursor.fetchone()
            cursor.close()

            # get the capacity of the airplane
            cursor = conn.cursor()
            query = "SELECT seats FROM airplane WHERE airplane_id = '{}'"
            cursor.execute(query.format(airplane_id))
            capacity = cursor.fetchone()
            cursor.close()

            max_ticket_id = latest_id['max_id'] if latest_id['max_id'] is not None else 0
            for i in range(1, int(capacity['seats'])+1):
                # add tickets for each seat on the flight
                cursor = conn.cursor()
                query = "INSERT INTO ticket VALUES ('{}', '{}', '{}')"
                cursor.execute(query.format(max_ticket_id + i, session['airline'], flight_num))
                conn.commit()
                cursor.close()

            flash('You have successfully added a new flight!', 'success')
            return redirect(url_for('dashboard_airline_staff'))

    return render_template('dashboard_airline_staff.html',
                           add_airplane_form=add_airplane_form,
                           add_airport_form=add_airport_form,
                           airline_staff_search_form=airline_staff_search_form,
                           flights=flights,
                           change_flight_status_form=change_flight_status_form,
                           grant_new_permission_form=grant_new_permission_form,
                           add_booking_agent_to_airline_form=add_booking_agent_to_airline_form,
                           create_flight_form=create_flight_form)

# define route for view customer
@app.route('/view_customer/<flight_num>', methods=['GET', 'POST'])
def view_customer(flight_num):
    cursor = conn.cursor()
    query = f"SELECT * FROM ticket T NATURAL JOIN purchases P LEFT JOIN customer C ON P.customer_email=C.email WHERE T.flight_num = '{flight_num}'"
    cursor.execute(query)
    customers = cursor.fetchall()
    cursor.close()

    return render_template('view_customer.html', flight_num=flight_num, customers=customers)


# @app.route('/create_flight', methods=['GET', 'POST'])
# def create_flight():

#     # handle illegal access
#     if 'permission_type' not in session:
#         flash('Please login as an airline staff first!', 'danger')
#         return redirect(url_for('login'))
#     elif 'Admin' not in session['permission_type']:
#         flash('You are not admin, so you are not authorized :(', 'danger')
#         return redirect(url_for('dashboard_airline_staff'))

#     create_flight_form = forms.CreateFlightForm()
#     if create_flight_form.validate_on_submit():
#         flight_num = create_flight_form.flight_num.data
#         departure_airport = create_flight_form.departure_airport.data
#         departure_time = create_flight_form.departure_time.data
#         arrival_airport = create_flight_form.arrival_airport.data
#         arrival_time = create_flight_form.arrival_time.data
#         price = create_flight_form.price.data
#         status = create_flight_form.status.data
#         airplane_id = create_flight_form.airplane_id.data

#         # check whether the flight exists
#         cursor = conn.cursor()
#         query = "SELECT * FROM flight WHERE flight_num = '{}'"
#         cursor.execute(query.format(flight_num))
#         data = cursor.fetchone()
#         cursor.close()
#         if data:
#             flash('The flight already exists!', 'danger')
#         else:
#             # add the flight to the database
#             cursor = conn.cursor()
#             query = "INSERT INTO flight VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
#             cursor.execute(query.format(session['airline'], flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id))
#             conn.commit()
#             cursor.close()

#             # check the existing ticket id:
#             cursor = conn.cursor()
#             query = "SELECT MAX(ticket_id) FROM ticket"
#             cursor.execute(query)
#             latest_id = cursor.fetchone()
#             cursor.close()
#             print("latest_id: ", latest_id)

#             # check the capacity of the flight
#             cursor = conn.cursor()
#             query = "SELECT seats FROM airplane WHERE airplane_id = '{}'"
#             cursor.execute(query.format(airplane_id))
#             capacity = cursor.fetchone()
#             cursor.close()
#             print("capacity: ", capacity)

#             for i in range(1, int(capacity['seats'])+1):
#                 # add tickets to the flight
#                 cursor = conn.cursor()
#                 query = "INSERT INTO ticket VALUES ('{}', '{}', '{}')"
#                 cursor.execute(query.format(int(latest_id['MAX(ticket_id)'])+i, session['airline'], flight_num))
#                 conn.commit()
#                 cursor.close()

#             flash('You have successfully added a new flight!', 'success')
#             return redirect(url_for('dashboard_airline_staff'))

#     return render_template('create_flight.html', create_flight_form=create_flight_form)

# define route for view all booking agents
@app.route('/view_all_booking_agents', methods=['GET', 'POST'])
def view_all_booking_agents():
    # 获取过去一个月内此航空公司基于售票数量的前5名预订代理
    cursor = conn.cursor()
    query = f"SELECT booking_agent_id, COUNT(*) AS num_tickets FROM purchases NATURAL JOIN ticket WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH ) AND booking_agent_id IS NOT NULL GROUP BY booking_agent_id ORDER BY num_tickets DESC LIMIT 5"
    cursor.execute(query)
    top_5_agents_past_month = cursor.fetchall()
    cursor.close()

    # 获取过去一年内此航空公司基于售票数量的前5名预订代理
    cursor = conn.cursor()
    query = f"SELECT booking_agent_id, COUNT(*) AS num_tickets FROM purchases NATURAL JOIN ticket WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) AND booking_agent_id IS NOT NULL GROUP BY booking_agent_id ORDER BY num_tickets DESC LIMIT 5"
    cursor.execute(query)
    top_5_agents_past_year = cursor.fetchall()
    cursor.close()

    # 获取过去一年内此航空公司基于佣金的前5名预订代理
    cursor = conn.cursor()
    query = f"SELECT booking_agent_id, SUM(price) AS commission FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) AND booking_agent_id IS NOT NULL GROUP BY booking_agent_id ORDER BY commission DESC LIMIT 5"
    cursor.execute(query)
    top_5_agents_commission_past_year = cursor.fetchall()
    cursor.close()

    # 获取此航空公司的所有预订代理
    cursor = conn.cursor()
    query = f"SELECT * FROM booking_agent NATURAL JOIN booking_agent_work_for WHERE airline_name = '{session['airline']}'"
    cursor.execute(query)
    booking_agents = cursor.fetchall()
    cursor.close()

    return render_template('view_all_booking_agents.html', 
                           top_5_agents_past_month=top_5_agents_past_month,
                           top_5_agents_past_year=top_5_agents_past_year,
                           top_5_agents_commission_past_year=top_5_agents_commission_past_year,
                           booking_agents=booking_agents)

# @app.route('/view_all_booking_agents', methods=['GET', 'POST'])
# def view_all_booking_agents():
#     # get top 5 booking agents based on number of tickets sales for the past month in this airline
#     cursor = conn.cursor()
#     query = f"SELECT booking_agent_id, COUNT(*) AS num_tickets FROM purchases NATURAL JOIN ticket WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH ) AND booking_agent_id IS NOT NULL GROUP BY booking_agent_id ORDER BY num_tickets DESC LIMIT 5"
#     cursor.execute(query)
#     top_5_agents_past_month = cursor.fetchall()
#     cursor.close()
#     # covert result to list
#     temp_dic = {'booking_agent_id': [], 'num_tickets': []}
#     for i in range(5):
#         try:
#             agent = top_5_agents_past_month[i]
#             temp_dic['booking_agent_id'].append(agent['booking_agent_id'])
#             temp_dic['num_tickets'].append(agent['num_tickets'])
#         except:
#             temp_dic['booking_agent_id'].append("Empty")
#             temp_dic['num_tickets'].append(0)
#     top_5_agents_past_month = temp_dic
#     print(top_5_agents_past_month)

#     # get top 5 booking agents based on number of tickets sales for the past year in this airline
#     cursor = conn.cursor()
#     query = f"SELECT booking_agent_id, COUNT(*) AS num_tickets FROM purchases NATURAL JOIN ticket WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) AND booking_agent_id IS NOT NULL GROUP BY booking_agent_id ORDER BY num_tickets DESC LIMIT 5"
#     cursor.execute(query)
#     top_5_agents_past_year = cursor.fetchall()
#     cursor.close()
#     # convert result to list
#     temp_dic = {'booking_agent_id': [], 'num_tickets': []}
#     for i in range(5):
#         try:
#             agent = top_5_agents_past_year[i]
#             temp_dic['booking_agent_id'].append(f"Agent ID: {agent['booking_agent_id']}")
#             temp_dic['num_tickets'].append(agent['num_tickets'])
#         except:
#             temp_dic['booking_agent_id'].append("Empty")
#             temp_dic['num_tickets'].append(0)
#     top_5_agents_past_year = temp_dic
#     print(top_5_agents_past_year)

#     # get top 5 booking agents based on commission for the past month in this airline
#     cursor = conn.cursor()
#     query = f"SELECT booking_agent_id, SUM(price) AS commission FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) AND booking_agent_id IS NOT NULL GROUP BY booking_agent_id ORDER BY commission DESC LIMIT 5"
#     cursor.execute(query)
#     top_5_agents_commission_past_year = cursor.fetchall()
#     cursor.close()
#     # convert result to list
#     temp_dic = {'booking_agent_id': [], 'commission': []}
#     for i in range(5):
#         try:
#             agent = top_5_agents_commission_past_year[i]
#             temp_dic['booking_agent_id'].append(f"Agent ID: {agent['booking_agent_id']}")
#             temp_dic['commission'].append(int(agent['commission']))
#         except:
#             temp_dic['booking_agent_id'].append("Empty")
#             temp_dic['commission'].append(0)
#     top_5_agents_commission_past_year = temp_dic
#     print(top_5_agents_commission_past_year)

#     # get all booking agents in this airline
#     cursor = conn.cursor()
#     query = f"SELECT * FROM booking_agent NATURAL JOIN booking_agent_work_for WHERE airline_name = '{session['airline']}'"
#     cursor.execute(query)
#     booking_agents = cursor.fetchall()
#     cursor.close()
#     print(booking_agents)

#     return render_template('view_all_booking_agents.html', top_5_agents_past_month=json.dumps(top_5_agents_past_month), top_5_agents_past_year=json.dumps(top_5_agents_past_year), top_5_agents_commission_past_year=json.dumps(top_5_agents_commission_past_year), booking_agents=booking_agents)

# define route for view frequent customers in the airline
@app.route('/frequent_customers', methods=['GET', 'POST'])
def frequent_customers():
    # get customers sorted by number of tickets purchased in the past year
    # only count for this airline
    cursor = conn.cursor()
    query = f"SELECT customer_email, COUNT(*) AS num_tickets FROM purchases NATURAL JOIN ticket WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) GROUP BY customer_email ORDER BY num_tickets DESC"
    cursor.execute(query)
    customers = cursor.fetchall()
    cursor.close()
    return render_template('frequent_customers.html', customers=customers)

# define route for view ticket
@app.route('/view_customer_tickets/<customer_email>', methods=['GET', 'POST'])
def view_customer_tickets(customer_email):
    # get all tickets purchased by this customer
    cursor = conn.cursor()
    query = f"SELECT * FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE customer_email = '{customer_email}' AND airline_name = '{session['airline']}'"
    cursor.execute(query)
    tickets = cursor.fetchall()
    cursor.close()
    return render_template('view_customer_tickets.html', tickets=tickets, customer_email=customer_email)

# define route for view reports
@app.route('/view_reports', methods=['GET', 'POST'])
def view_reports():
    class ViewTicketReportsForm(FlaskForm):
        identifier = StringField('Identifier')
        start_date = DateField('Start Date', validators=[])
        end_date = DateField('End Date', validators=[])
        submit = SubmitField('View Reports')

    form_view_ticket_reports = ViewTicketReportsForm()
    # Total amounts of ticket sold based on range of dates
    # Month wise tickets sold in a bar chart
    start_date = datetime.date.today() - relativedelta(years=1) if form_view_ticket_reports.start_date.data == None else form_view_ticket_reports.start_date.data
    end_date = datetime.date.today() if form_view_ticket_reports.end_date.data == None else form_view_ticket_reports.end_date.data
    cursor = conn.cursor()
    query = f"SELECT YEAR(purchase_date) AS year, MONTH(purchase_date) AS month, COUNT(*) AS num_tickets FROM purchases NATURAL JOIN ticket WHERE airline_name = '{session['airline']}' AND purchase_date >= '{start_date}' AND purchase_date <= '{end_date}' GROUP BY year, month"
    cursor.execute(query)
    tickets_report = cursor.fetchall()
    cursor.close()

    # convert result to list
    temp_dic = {'year-month': [], 'num_tickets': []}
    while start_date <= end_date:
        temp_dic['year-month'].append(f"{start_date.year}-{start_date.month}")
        data_exits = False
        for ticket in tickets_report:
            if ticket['year'] == start_date.year and ticket['month'] == start_date.month:
                temp_dic['num_tickets'].append(ticket['num_tickets'])
                data_exits = True
                break
        if not data_exits:
            temp_dic['num_tickets'].append(0)
        start_date += relativedelta(months=1)

    tickets_report = temp_dic
    return render_template('view_reports.html', form_view_ticket_reports=form_view_ticket_reports, tickets_report=json.dumps(tickets_report))


@app.route('/view_compare_revenue', methods=['GET', 'POST'])
def view_compare_revenue():
    # showing total amount of revenue earned from direct sales (when customer bought tickets without using a booking agent)
    # and total amount of revenue earned from indirect sales (when customer bought tickets using booking agents) in the last month and last year

    # get total revenue from direct sales in the past month
    cursor = conn.cursor()
    query = f"SELECT SUM(price) AS revenue FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH ) AND booking_agent_id IS NULL"
    cursor.execute(query)
    direct_sales_past_month = cursor.fetchone()['revenue']
    if direct_sales_past_month is None:
        direct_sales_past_month = 0
    cursor.close()
    # get total revenue from direct sales in the past year
    cursor = conn.cursor()
    query = f"SELECT SUM(price) AS revenue FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) AND booking_agent_id IS NULL"
    cursor.execute(query)
    direct_sales_past_year = cursor.fetchone()['revenue']
    if direct_sales_past_year is None:
        direct_sales_past_year = 0
    cursor.close()

    # get total revenue from indirect sales in the past month
    cursor = conn.cursor()
    query = f"SELECT SUM(price) AS revenue FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH ) AND booking_agent_id IS NOT NULL"
    cursor.execute(query)
    indirect_sales_past_month = cursor.fetchone()['revenue']
    if indirect_sales_past_month is None:
        indirect_sales_past_month = 0
    cursor.close()

    # get total revenue from indirect sales in the past year
    cursor = conn.cursor()
    query = f"SELECT SUM(price) AS revenue FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) AND booking_agent_id IS NOT NULL"
    cursor.execute(query)
    indirect_sales_past_year = cursor.fetchone()['revenue']
    if indirect_sales_past_year is None:
        indirect_sales_past_year = 0
    cursor.close()

    return render_template('view_compare_revenue.html', direct_sales_revenue_past_month=direct_sales_past_month, direct_sales_revenue_past_year=direct_sales_past_year, indirect_sales_revenue_past_month=indirect_sales_past_month, indirect_sales_revenue_past_year=indirect_sales_past_year)

@app.route('/view_top_destinations', methods=['GET', 'POST'])
def view_top_destinations():
    # get top 3 destinations in the past month
    cursor = conn.cursor()
    query = f"SELECT airport_name AS destination, COUNT(*) AS num_tickets FROM purchases NATURAL JOIN ticket NATURAL JOIN flight JOIN airport ON flight.arrival_airport = airport.airport_name WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH ) GROUP BY destination ORDER BY num_tickets DESC LIMIT 3"
    cursor.execute(query)
    top_destinations_past_month = cursor.fetchall()
    cursor.close()

    # get top 3 destinations in the past year
    cursor = conn.cursor()
    query = f"SELECT airport_name AS destination, COUNT(*) AS num_tickets FROM purchases NATURAL JOIN ticket NATURAL JOIN flight JOIN airport ON flight.arrival_airport = airport.airport_name WHERE airline_name = '{session['airline']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) GROUP BY destination ORDER BY num_tickets DESC LIMIT 3"
    cursor.execute(query)
    top_destinations_past_year = cursor.fetchall()
    cursor.close()
    return render_template('view_top_destinations.html', top_destinations_past_month=top_destinations_past_month, top_destinations_past_year=top_destinations_past_year)


@app.route('/view_top_customers', methods=['GET', 'POST'])
def view_all_customers():

    # get top 5 customers based on number of tickets sales for the past 6 months
    cursor = conn.cursor()
    query = f"SELECT customer_email, COUNT(*) AS num_tickets FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH ) GROUP BY customer_email ORDER BY num_tickets DESC LIMIT 5 "
    cursor.execute(query)
    top_5_customers_past_month = cursor.fetchall()
    cursor.close()
    # covert result to list
    temp_dic = {'customer_email': [], 'num_tickets': []}
    for i in range(5):
        try:
            cust = top_5_customers_past_month[i]
            temp_dic['customer_email'].append(cust['customer_email'])
            temp_dic['num_tickets'].append(cust['num_tickets'])
        except:
            temp_dic['customer_email'].append("Empty")
            temp_dic['num_tickets'].append(0)
    top_5_customers_past_month = temp_dic
    # get top 5 customers based on commission for the past year
    cursor = conn.cursor()
    query = f"SELECT customer_email, SUM(price) * 0.1 AS commission FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']}' AND purchase_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR ) GROUP BY customer_email ORDER BY commission DESC LIMIT 5"
    cursor.execute(query)
    top_5_commissions_past_year = cursor.fetchall()
    cursor.close()
    # convert result to list
    temp_dic = {'customer_email': [], 'commission': []}
    for i in range(5):
        try:
            cust = top_5_commissions_past_year[i]
            temp_dic['customer_email'].append(cust['customer_email'])
            temp_dic['commission'].append(int(cust['commission']))
        except:
            temp_dic['customer_email'].append("Empty")
            temp_dic['commission'].append(0)
    top_5_commissions_past_year = temp_dic


    return render_template('view_all_customers.html', top_5_customers_past_month=json.dumps(top_5_customers_past_month), top_5_commissions_past_year=json.dumps(top_5_commissions_past_year))


@app.route('/view_commissions', methods=['GET', 'POST'])
def view_commissions():
    class ViewCommissionsForm(FlaskForm):
        identifier = StringField('Identifier')
        start_date = DateField('Start Date', validators=[])
        end_date = DateField('End Date', validators=[])
        submit = SubmitField('View Reports')

    form_view_commissions_reports = ViewCommissionsForm()
    # Total amounts of ticket sold based on range of dates
    # Month wise tickets sold in a bar chart
    start_date = datetime.date.today() - relativedelta(month=1) if form_view_commissions_reports.start_date.data == None else form_view_commissions_reports.start_date.data
    end_date = datetime.date.today() if form_view_commissions_reports.end_date.data == None else form_view_commissions_reports.end_date.data
    cursor = conn.cursor()
    query = f"SELECT COUNT(*) AS num_tickets FROM purchases NATURAL JOIN ticket WHERE booking_agent_id = '{session['agent_id']}' AND purchase_date >= '{start_date}' AND purchase_date <= '{end_date}' "
    cursor.execute(query)
    ticket_num = cursor.fetchone()['num_tickets']
    cursor.close()

    cursor = conn.cursor()
    query = f"SELECT SUM(price)*0.1 AS sum_commissions FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE booking_agent_id = '{session['agent_id']}' AND purchase_date >= '{start_date}' AND purchase_date <= '{end_date}' "
    cursor.execute(query)
    commissions_sum = cursor.fetchone()['sum_commissions']
    cursor.close()

    try:
        commissions_avg = float(commissions_sum)/float(ticket_num)
    except:
        commissions_avg = None
        commissions_sum = 0

    return render_template('view_commissions.html', form_view_commissions_reports=form_view_commissions_reports, ticket_num = ticket_num,commissions_sum = commissions_sum, commissions_avg = commissions_avg)


@app.route('/purchase/<flight_num>', methods=['GET', 'POST'])
def purchase(flight_num):
    class PurchaseCus(FlaskForm):
        customer = StringField('Your Email', validators=[])
        submit = SubmitField('Purchase')
    class PurchaseAgen(FlaskForm):
        customer = StringField('Email of your customer', validators=[DataRequired(), Email(), Length(min=1, max=50)])
        agent = StringField('Agent_ID', validators=[])
        submit = SubmitField('Purchase')

    if 'status' not in session:
        return redirect(url_for('home'))
    else:
        if session['status'] == 'customer':
            status = 'customer'
            form = PurchaseCus()
        elif session['status'] == 'agent':
            status = 'agent'
            form = PurchaseAgen()
        else:
            return redirect(url_for('home'))
    #get flight info
    cursor = conn.cursor()
    query = f"SELECT * FROM ticket NATURAL JOIN flight WHERE flight_num = '{flight_num}'"
    cursor.execute(query)
    flight = cursor.fetchone()
    cursor.close()

    #get status

    #get seat info
    cursor = conn.cursor()
    query = f"SELECT count(ticket_id) as leftt\
                FROM (ticket AS t natural join flight)\
                where flight_num = '{flight_num}' and \
                not exists(SELECT *\
                    FROM purchases as p\
                    WHERE p.ticket_id = t.ticket_id)"
    cursor.execute(query)
    left = cursor.fetchone()
    cursor.close()
    
    cursor = conn.cursor()
    query = f"SELECT count(ticket_id) as alll\
            FROM ticket AS t natural join flight\
            where flight_num = '{flight_num}'\
            group by flight_num;"
    cursor.execute(query)
    all = cursor.fetchone()
    cursor.close()
    if form.validate_on_submit():
        
        #updating seat info
        cursor = conn.cursor()
        query = f"SELECT count(ticket_id) as leftt\
                    FROM (ticket AS t natural join flight)\
                    where flight_num = '{flight_num}' and \
                    not exists(SELECT *\
                        FROM purchases as p\
                        WHERE p.ticket_id = t.ticket_id)"
        cursor.execute(query)
        left = cursor.fetchone()
        cursor.close()
        
        cursor = conn.cursor()
        query = f"SELECT count(ticket_id) as alll\
                FROM ticket AS t natural join flight\
                where flight_num = '{flight_num}'\
                group by flight_num;"
        cursor.execute(query)
        all = cursor.fetchone()
        cursor.close()
        if session['status'] == 'customer':
            form.customer.data = customer = session['email']
            agent = None
        else:
            customer = form.customer.data
            form.agent.data = agent = session['agent_id']

        cursor = conn.cursor()
        query_find_avil_ticket = "SELECT * FROM ticket AS t WHERE flight_num = '{}' and not exists \
                                        (SELECT * FROM purchases AS p WHERE p.ticket_id = t.ticket_id)"
        cursor.execute(query_find_avil_ticket.format(flight_num))
        found = cursor.fetchall()

        # flash(f'Purchasing Ticket from {flight_num}  {found}!', 'success')
        if len(found) == 0:
            flash('ticket not found', 'danger')
            cursor.close()
        else:
            airline_name = found[0]["airline_name"]
            flight_num = found[0]["flight_num"]
            ticket_id = found[0]["ticket_id"]

            #make sure agent correct
            if agent is not None:
                cursor = conn.cursor()
                query_find_airline = "SELECT * FROM booking_agent natural JOIN booking_agent_work_for WHERE booking_agent_id = '{}' and airline_name = '{}' "
                cursor.execute(query_find_airline.format(agent,airline_name))
                work_for = cursor.fetchall()


            #make sure customer correct
            cursor = conn.cursor()
            query_find_airline = "SELECT * FROM customer WHERE email = '{}'"
            cursor.execute(query_find_airline.format(customer))
            cus = cursor.fetchall()

            if agent is not None and len(work_for) == 0:
                flash("You are not working for this airline!","danger")

            else:
                if len(cus) == 0:
                    flash("Customer_ID incorrect","danger")
                else:

                    date = datetime.date.today()
                    if agent is None:
                        query = f"INSERT INTO purchases VALUES ('{ticket_id}', '{customer}', NULL, '{date}')"
                    else:
                        query = f"INSERT INTO purchases VALUES ('{ticket_id}', '{customer}', '{agent}', '{date}')"
                    cursor.execute(query)
                    conn.commit()
                    flash(f'User {session["email"]} Purchased Ticket {ticket_id} from {flight_num} at {airline_name} !', 'success')
                    cursor.close()
                    return redirect(url_for('home'))

    if status == 'customer':
        return render_template('customer_purchase.html',form = form,flight = flight,left = left,all = all)
    elif status == 'agent':
        return render_template('agent_purchase.html',form = form,flight = flight,left = left,all = all)



# @app.route('/view_customer_tickets/<customer_email>', methods=['GET', 'POST'])
# def view_customer_tickets(customer_email):
#     # get all tickets purchased by this customer
#     cursor = conn.cursor()
#     query = f"SELECT * FROM purchases NATURAL JOIN ticket NATURAL JOIN flight WHERE customer_email = '{customer_email}' AND airline_name = '{session['airline']}'"
#     cursor.execute(query)
#     tickets = cursor.fetchall()
#     cursor.close()
#     print(tickets)
#     return render_template('view_customer_tickets.html', tickets=tickets, customer_email=customer_email)

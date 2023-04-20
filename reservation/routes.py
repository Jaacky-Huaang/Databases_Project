from flask import render_template, request, url_for, redirect, session, flash
from reservation import app, conn, bcrypt
import reservation.forms as forms
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    # public search
    form_upcoming_flight = forms.PublicSearchUpcomingFlightForm()
    if form_upcoming_flight.validate_on_submit():
        departure_place = form_upcoming_flight.departure_place.data
        arrival_place = form_upcoming_flight.arrival_place.data
        departure_time = form_upcoming_flight.departure_time.data
        arrival_time = form_upcoming_flight.arrival_time.data

        cursor = conn.cursor()
        query_upcoming_flight = f'SELECT * FROM flight F LEFT JOIN airport A1 ON F.departure_airport = A1.airport_name LEFT JOIN airport A2 ON F.arrival_airport = A2.airport_name NATURAL JOIN airplane P WHERE (A1.airport_name LIKE "%{departure_place}%" OR A1.airport_city LIKE "%{departure_place}%") AND (A2.airport_name LIKE "%{arrival_place}%" OR A2.airport_city LIKE "%{arrival_place}%") AND F.departure_time LIKE "%{departure_time}%" AND F.arrival_time LIKE "%{arrival_time}%"'
        cursor.execute(query_upcoming_flight)
        search_result = cursor.fetchall()
        cursor.close()
        if len(search_result) == 0:
            flash('No flight found', 'danger')
        else:
            return redirect(url_for('upcoming_flight', search_result=json.dumps(search_result, default=str)))

    form_flight_status = forms.PublicSearchFlightStatusForm()
    flight_number = '' if form_flight_status.flight_number.data==None else form_flight_status.flight_number.data
    departure_time = '' if form_flight_status.departure_time.data==None else form_flight_status.departure_time.data
    arrival_time = '' if form_flight_status.arrival_time.data==None else form_flight_status.arrival_time.data
    cursor = conn.cursor()
    query_flight_status = f'SELECT * FROM flight WHERE flight_num LIKE "%{flight_number}%" AND departure_time LIKE "%{departure_time}%" AND arrival_time LIKE "%{arrival_time}%"'
    cursor.execute(query_flight_status)
    status_search_result = cursor.fetchall()
    cursor.close()

    return render_template('index.html', form_upcoming_flight=form_upcoming_flight, form_flight_status=form_flight_status, status_search_result=status_search_result)


@app.route('/about')
def about():
    return render_template('about.html')

# Define route for searching upcoming flight
@app.route('/upcoming_flight/<search_result>', methods=['GET', 'POST'])
def upcoming_flight(search_result):
    search_result = json.loads(search_result)
    # print(type(search_result[0]))
    return render_template('upcoming_flight.html', search_result=search_result)



# Define route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    form = forms.CustomerRegistrationForm()

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


@app.route('/register_agent', methods=['GET', 'POST'])
def register_agent():
    form = forms.BookingAgentRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        booking_agent_id = form.booking_agent_id.data

        cursor = conn.cursor()
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


@app.route('/register_airline_staff', methods=['GET', 'POST'])
def register_airline_staff():
    form = forms.StaffRegistrationForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        first_name = form.first_name.data
        last_name = form.last_name.data
        date_of_birth = form.date_of_birth.data
        airline_name = form.airline_name.data

        cursor = conn.cursor()
        query_find_user_name = "SELECT user_name FROM airline_staff WHERE user_name = '{}'"
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/login_customer', methods=['GET', 'POST'])
def login_customer():
    form = forms.CustomerLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = conn.cursor()
        query = "SELECT * FROM customer WHERE email = '{}'"
        cursor.execute(query.format(email))
        data = cursor.fetchone()
        cursor.close()

        if data and bcrypt.check_password_hash(data[2], password):
            # add the customer email to the session
            session['email'] = email
            # add the user status to the session
            session['status'] = 'customer'

            return redirect(url_for('home'))  # Change later
        elif not data:  # handle the case when the email does not exist
            flash('Email does not exist!', 'danger')
        else:  # handle the case when the password is wrong
            flash('Wrong password. Please enter the password again.', 'danger')

    return render_template('login_customer.html', title='Login as Customer', form=form)


@app.route('/login_agent', methods=['GET', 'POST'])
def login_agent():
    form = forms.BookingAgentLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        cursor = conn.cursor()
        query = "SELECT * FROM booking_agent WHERE email = '{}'"
        cursor.execute(query.format(email))
        data = cursor.fetchone()
        cursor.close()

        if data and bcrypt.check_password_hash(data[1], password):
            # add the agent email to the session
            session['email'] = email
            # add the user status to the session
            session['status'] = 'agent'
            flash(f'You have successfully logged in as {email}!', 'success')

            return redirect(url_for('home'))  # Change later
        elif not data:  # handle the case when the email does not exist
            flash('Email does not exist!', 'danger')
        else:  # handle the case when the password is wrong
            flash('Wrong password. Please enter the password again.', 'danger')

    return render_template('login_agent.html', title='Login as Agent', form=form)


@app.route('/login_airline_staff', methods=['GET', 'POST'])
def login_airline_staff():
    form = forms.StaffLoginForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data

        cursor = conn.cursor()
        query = "SELECT * FROM airline_staff WHERE user_name = '{}'"
        cursor.execute(query.format(user_name))
        data = cursor.fetchone()
        cursor.close()

        if data and bcrypt.check_password_hash(data[1], password):
            # add the staff user name to the session
            session['user_name'] = user_name
            # add the user status to the session
            session['status'] = 'airline_staff'

            return redirect(url_for('home'))  # also change here later

        elif not data:  # handle the case when the email does not exist
            flash('Username does not exist!', 'danger')
        else:  # handle the case when the password is wrong
            flash('Wrong password. Please enter the password again.', 'danger')

    return render_template('login_airline_staff.html', title='Login as Airline Staff', form=form)


@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('user_name', None)
    session.pop('status', None)
    flash('You have successfully logged out!', 'secondary')
    return redirect(url_for('home'))




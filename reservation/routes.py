from flask import render_template, request, url_for, redirect, session, flash
from reservation import app, conn, bcrypt
import reservation.forms as forms

@app.route('/')
@app.route('/home')
def home():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

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

    return render_template('register_customer.html', title='Register', form=form)


@app.route('/register_agent', methods=['GET', 'POST'])
def register_agent():
    return render_template('register_agent.html')


@app.route('/register_airline_staff', methods=['GET', 'POST'])
def register_airline_staff():
    return render_template('register_airline_staff.html')


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
            session['email'] = email
            return redirect(url_for('home'))  # Change later
        elif not data:  # handle the case when the email does not exist
            flash('Email does not exist!', 'danger')
        else:  # handle the case when the password is wrong
            flash('Wrong password. Please enter the password again.', 'danger')

    return render_template('login_customer.html', title='Login', form=form)


@app.route('/login_agent', methods=['GET', 'POST'])
def login_agent():
    return render_template('login_agent.html')


@app.route('/login_airline_staff', methods=['GET', 'POST'])
def login_airline_staff():
    return render_template('login_airline_staff.html')
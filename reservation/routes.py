from flask import render_template, request, url_for, redirect, session, flash
from reservation import app
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
        password = form.password.data
        building_number = form.building_number.data
        street = form.street.data
        city = form.city.data
        state = form.state.data
        # phone_number = form.phone_number.data
        phone_number = 5555551212
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
            query = "INSERT INTO customer VALUES ('{}', '{}', md5('{}'), '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"
            cursor.execute(query.format(email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
            conn.commit()
            flash(f'Account created for {form.name.data}!', 'success')
            cursor.close()
            return redirect(url_for('home'))

    return render_template('register_customer.html', title='Register', form=form)


@app.route('/register_agent', methods=['GET', 'POST'])
def register_agent():
    return render_template('register_agent.html')


@app.route('/register_airline_staff', methods=['GET', 'POST'])
def register_airline_staff():
    return render_template('register_airline_staff.html')
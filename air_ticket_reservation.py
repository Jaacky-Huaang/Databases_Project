from flask import Flask, render_template, request, url_for, redirect, session
import mysql.connector

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password='',
                               database='ticket_reservation')

# Define a route to hello function
@app.route('/')
def hello():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('index.html')
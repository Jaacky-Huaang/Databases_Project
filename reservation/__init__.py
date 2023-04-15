# Import Flask Library
from flask import Flask
import mysql.connector

# Import our python files
# import forms

# Initialize the app from Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '24c34e0557b4cddff58f81952034d281'

# Configure MySQL
conn = mysql.connector.connect(host='localhost',
                               user='root',
                               password='',
                               database='ticket_reservation')

from reservation import routes

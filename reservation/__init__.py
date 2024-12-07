# Import Flask Library
from flask import Flask
from flask_bcrypt import Bcrypt
# import mysql.connector
import pymysql.cursors

# Import our python files
# import forms

# Initialize the app from Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '24c34e0557b4cddff58f81952034d281'

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       database='ticket_reservation',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt(app)

from reservation import routes

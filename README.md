# CSCI-SHU-213-Database-Final-Project
> Ricercar & Jason

 To build an online Air Ticket Reservation System

## Getting Started
### Packages
* flask
* flask-wtf
* flask-bcrypt
* python-dateutil

Run ``pip install required package.txt`` to install the required packages, and start XAMPP server on your local machine

### Start the server
1. Create the database called ``ticket_reservation`` using ``Solution_ProjectPart2_create_tables_Fall_2021_v1.sql``
2. Insert data using ``insert.sql``
3. Run the python file in terminal with``python3 run.py``
4. Go to ``http://127.0.0.1:5000`` in your browser (we set the port to be 5000 by default)

## Resources
### A Simple Flask Tutorial by Corey Schafer
* [Flask Tutorial](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)
* [Flask Tutorial Source Code](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog)

### Example Project
* https://github.com/Jaxingjili/NYU-Database-Project_2022

### Imported Package Documentations
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [wtforms](https://wtforms.readthedocs.io/en/3.0.x/)
* [bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/)

### Bootstrap example code
* https://getbootstrap.com/docs/5.2/examples/

## Webui Design Inspirations
* https://wwws.airfrance.com.cn/
* https://www.cathaypacific.com/cx/en_HK.html
* https://www.skyscanner.com.hk/?&associateID=SEM_GGF_19370_00062

## File Structure
*Last Update: 2023.5.7*
```
├── Project_3.pdf
├── README.md
├── Solution_ProjectPart2_create_tables_Fall_2021_v1.sql
├── insert.sql
├── required package.txt
├── reservation
│   ├── __init__.py
│   ├── forms.py
│   ├── query.sql
│   ├── routes.py
│   ├── static
│   │   ├── assets
│   │   │   ├── brand
│   │   │   │   ├── bootstrap-logo-white.svg
│   │   │   │   └── bootstrap-logo.svg
│   │   │   └── dist
│   │   │       ├── css
│   │   │       │   ├── bootstrap.min.css
│   │   │       │   ├── bootstrap.min.css.map
│   │   │       │   ├── bootstrap.rtl.min.css
│   │   │       │   └── bootstrap.rtl.min.css.map
│   │   │       └── js
│   │   │           ├── bootstrap.bundle.min.js
│   │   │           └── bootstrap.bundle.min.js.map
│   │   └── main.css
│   └── templates
│       ├── about.html
│       ├── agent_purchase.html
│       ├── create_flight.html
│       ├── customer_purchase.html
│       ├── dashboard_agent.html
│       ├── dashboard_airline_staff.html
│       ├── dashboard_customer.html
│       ├── frequent_customers.html
│       ├── index.html
│       ├── layout.html
│       ├── login.html
│       ├── login_agent.html
│       ├── login_airline_staff.html
│       ├── login_customer.html
│       ├── register.html
│       ├── register_agent.html
│       ├── register_airline_staff.html
│       ├── register_customer.html
│       ├── upcoming_flight.html
│       ├── view_all_booking_agents.html
│       ├── view_all_customers.html
│       ├── view_commissions.html
│       ├── view_compare_revenue.html
│       ├── view_customer.html
│       ├── view_customer_tickets.html
│       ├── view_reports.html
│       └── view_top_destinations.html
└── run.py
```

## Change Log
* Change the password to varchar(60) to handle the hash password
* Add foreign key constraint to agent in purchases table

## Team Work Plan
### Jinhong Xia
* Create the database and make up testing data
* Outline all required works into a checklist, and test all functions
* Code functions for ticket purchasing
* Code functions for booking agent
### Yuanhe Guo
* Build up the file structure
* Design the basic layout
* Code functions for public search
* Code functions for customer (except ticket purchasing)
* Code functions for airline staff

## Function Check List
### public search
- [x] upcoming flight, city/airport, date
- [x] flights status flight number, arrival/departure date

### login/register
- [x] login
- [x] register

### customer
- [x] purchased flight info (specify optionally) **Haven't done the optional yet**
    bug: purchase each time when refresh page
    do the form group need action? (to refresh probably)
- [x] purchase ticket (as long as there is room (capacity and ticket))
- [x] search for flight
- [x] track spending
- [x] logout
### agent
- [x] purchased flight info (specify optionally) same
- [x] purchase ticket (only for its airline)
- [x] search for flight
- [x] commission spending same
- [x] top customer same
- [x] logout
### airline stuff
- [x] view flights
- [x] create flights (check the seat and number of ticket)
- [x] change status of flight
- [x] add airplane
- [x] add airport
- [x] view all booking agents
- [x] view frequent customers
- [x] view tickets reports
- [x] comparison of revenue
- [x] top destination
- [x] grand permissions(only for "Admin") to other stuffs
- [x] add new booking agent(only for "Admin") to its airline

### permission
#### admin
- [x] add new airplane to its airline
- [x] add new airplanes and new flight
#### operator
- [x] set in progress flight's status


## Extra Points
### SQL:
* Vague Search using LIKE query
* Use date operations to specify a date

### UI Design:
* Bootstrap5 API
* Collapsible Side Bar
* Flash messages with flask
* Warnings for form validation
* Specially designed homepage with carousels
* Specially designed user interface for Tickets
* Banners with illustrations from behance
* Bar chart and Pie chart with chart.js

### Others:
* Block direct access to pages that require login using Session
* Use WTForm to validate form
* Use a base template to avoid code duplication
* Use the encryption and decryption functions from flask-bcrypt to protect the password
* Structure files as a package for better organization

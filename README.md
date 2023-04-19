# CSCI-SHU-213-Database-Final-Project
> Ricercar & Jason

 To build an online Air Ticket Reservation System

## Getting Started
### Packages
* flask
* flask-wtf
* flask-bcrypt

### Start the server
1. Create the database
2. Run the python file ``python3 run.py``

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
*Last Update: 2023.4.16*
```
├── Project_3.pdf
├── README.md
├── Solution_ProjectPart2_create_tables_Fall_2021_v1.sql
├── reservation
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   ├── forms.cpython-38.pyc
│   │   └── routes.cpython-38.pyc
│   ├── forms.py
│   ├── routes.py
│   ├── static
│   │   └── main.css
│   └── templates
│       ├── about.html
│       ├── index.html
│       ├── layout.html
│       ├── login.html
│       ├── login_customer.html
│       ├── register.html
│       └── register_customer.html
└── run.py
```

## testing merge
test1

## Notes
* Change the password to varchar(60) to handle the hash password


## Check List
### public search
- [ ] upcoming flight, city/airport, date
- [ ] flights status flight number, arrival/departure date

### login/register
- [x] login
- [x] register

### customer
- [ ] purchased flight info (specify optionally) 
- [ ] purchase ticket (as long as there is room (capacity and ticket))
- [ ] search for flight
- [ ] track spending
- [ ] logout
### agent
- [ ] purchased flight info (specify optionally) 
- [ ] purchase ticket (only for its airline)
- [ ] search for flight
- [ ] commission spending
- [ ] top customer
- [ ] logout
### airline stuff
- [ ] view flights
- [ ] create flights
- [ ] change status of flight
- [ ] add airplane
- [ ] add airport
- [ ] view all booking agents
- [ ] view frequent customers
- [ ] view tickets reports
- [ ] comparison of revenue
- [ ] top destination
- [ ] grand permissions(only for "Admin") to other stuffs
- [ ] add new booking agent(only for "Admin") to its airline

### permission
#### admin
- [ ] add new airplane to its airline
- [ ] add new airplanes and new flight
#### operator
- [ ] set in progress flight's status
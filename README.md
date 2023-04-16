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

## Notes
* Change the password to varchar(60) to handle the hash password
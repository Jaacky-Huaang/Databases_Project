
delete from booking_agent_work_for;
delete from permission;
delete from purchases;
delete from Airline_Staff;
delete from Customer;
delete from Booking_agent;
delete from Ticket;
delete from Flight;
delete from Airport;
delete from Airplane;
delete from Airline;

insert into Airline values("CE");
insert into Airline values("JA");


insert into Airport values("JFK", "NYC");
insert into Airport values("PVG", "SH");
insert into Customer values("123@123.com","Alice","$2b$12$QH7HxpFhSs1G7m5/s7tHK.nsTsztKZj8MjDWW1rtgHHKwp3HQd7qC",
                        "5","Century Avenue","Shanghai","China",
                        "123333123","EL12312","2029-3-10","China",
                        "2000-01-01");
insert into Customer values("567@123.com","Bob","$2b$12$QH7HxpFhSs1G7m5/s7tHK.nsTsztKZj8MjDWW1rtgHHKwp3HQd7qC",
                        "2","Yangsi Road","Shanghai","China",
                        "123111123","EL87992","2029-3-10","China",
                        "2001-01-09");
insert into Booking_agent values("890@gmail.com",
                         "$2b$12$QH7HxpFhSs1G7m5/s7tHK.nsTsztKZj8MjDWW1rtgHHKwp3HQd7qC",
                         "190000");
insert into Airplane values("CE", "1","89");
insert into Airplane values("CE", "2","89");
insert into Airplane values("JA", "3","89");
insert into Airline_Staff values("Jack Goodman", "$2b$12$QH7HxpFhSs1G7m5/s7tHK.nsTsztKZj8MjDWW1rtgHHKwp3HQd7qC",
                            "Jack",
                            "Goodman","1988-02-07","CE");
insert into Airline_Staff values("John", "$2b$12$QH7HxpFhSs1G7m5/s7tHK.nsTsztKZj8MjDWW1rtgHHKwp3HQd7qC",
                            "John",
                            "Goodman","1981-06-08","CE");

insert into Flight values("CE","906677","JFK","2023-01-01 00:00:02","PVG",
                        "2023-01-01 00:15:02","660","in_progress",
                        "1");

insert into Flight values("CE","903377","JFK","2023-02-01 00:00:02","PVG",
                        "2023-02-1 00:15:02","660","upcoming",
                        "2");

insert into Flight values("JA","901177","JFK","2023-01-02 00:00:02","PVG",
                        "2023-01-02 00:15:02","660","delayed",
                        "3");
insert into Ticket values("11","CE","903377");
insert into Ticket values("12","CE","903377");
insert into Ticket values("13","CE","903377");
insert into Ticket values("21","CE","906677");
insert into Ticket values("22","CE","906677");
insert into Ticket values("23","CE","906677");
insert into Ticket values("31","JA","901177");
insert into Ticket values("32","JA","901177");
insert into Ticket values("33","JA","901177");



insert into purchases values("11","123@123.com",null,"2023-5-01");
insert into purchases values("13","567@123.com","190000","2023-5-01");
insert into purchases values("23","567@123.com","190000","2023-4-15");


insert into booking_agent_work_for values("890@gmail.com","CE");
insert into booking_agent_work_for values("890@gmail.com","JA");
insert into permission values("Jack Goodman","Admin");
-- insert into permission values("Jack Goodman","Operator");
insert into permission values("John","Operator");
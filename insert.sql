
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

-- insert into AirlineStuff values("a",)

insert into Airport values("JFK", "NYC");
insert into Airport values("PVG", "SH");
-- insert into Customer values("123@123.com","Alice","123456",
--                         "5","Century Avenue","Shanghai","China",
--                         "123333123","EL12312","2029-3-10","China",
--                         "2000-01-01");
-- insert into Customer values("567@123.com","Bob","123321",
--                         "2","Yangsi Road","Shanghai","China",
--                         "123111123","EL87992","2029-3-10","China",
--                         "2001-01-09");
-- insert into Booking_agent values("890@gmail.com", "909090","19-0000");
insert into Airplane values("CE", "1","89");
insert into Airplane values("CE", "2","89");
-- insert into AirlineStuff values("Jack Goodman", "098908","Jack",
--                             "Goodman","1988-02-07","CE");
insert into Flight values("CE","906677","JFK","2023-01-01 00:00:02","PVG",
                        "2023-01-01 00:15:02","660","in_progress",
                        "1");

insert into Flight values("CE","903377","JFK","2023-02-01 00:00:02","PVG",
                        "2023-02-1 00:15:02","660","upcoming",
                        "2");

insert into Flight values("CE","901177","JFK","2023-01-02 00:00:02","PVG",
                        "2023-01-02 00:15:02","660","delayed",
                        "2");
insert into Ticket values("11","CE","903377");
insert into Ticket values("12","CE","903377");
insert into Ticket values("13","CE","903377");
insert into Ticket values("21","CE","901177");
insert into Ticket values("22","CE","901177");
insert into Ticket values("23","CE","901177");
-- insert into purchases values("1-1","123@123.com",null,"2022-12-01");
-- insert into purchases values("1-3","567@123.com","890@gmail.com","2022-12-01");
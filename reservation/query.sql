
-- find available ticket
SELECT * 
FROM ticket AS t
WHERE flight_num = '901177' and not exists 
        (SELECT * FROM purchases AS p WHERE p.ticket_id = t.ticket_id);


-- check agent work
SELECT * FROM booking_agent natural JOIN booking_agent_work_for WHERE booking_agent_id = 190000 and airline_name = 'CE';


--query ticket info
SELECT *
FROM ticket AS t natural join flight
where ticket_id = '12';


-- CE	903377	12	JFK	2023-02-01 00:00:02	PVG	2023-02-01 00:15:02	660	upcoming	2	


--get all ticket number according to flight_num
SELECT count(ticket_id)
FROM ticket AS t natural join flight
where flight_num = "901177"
group by flight_num;

--get rest ticket
SELECT count(ticket_id)
FROM (ticket AS t natural join flight)
where flight_num = "901177" and not exists(
    SELECT *
    FROM purchases as p
    WHERE p.ticket_id = t.ticket_id
)
group by flight_num;


                <a href = {{ url_for("purchase") }} >
                    <button type="submit" class="btn btn-outline-secondary">Purchase</button>
                </a>
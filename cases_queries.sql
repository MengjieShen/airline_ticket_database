-- ----------------------------------------------VIEW PUBLIC INFO-----------------------------------------------------------------------------------

-- 1. Search for upcoming flights based on source city/airport name, destination city/airport name, date.
-- This is implemeneted through the function SearchFlightThroughDateAuth()

-- @app.route('/SearchFlightThroughDateAuth', methods=['GET', 'POST'])
-- def SearchFlightThroughDateAuth():

SELECT *
FROM flight, airport
WHERE flight.departure_airport = airport.airport_name and (departure_airport = 'SFO' OR airport_city = 'SFO') 
	and datediff(flight.departure_time, "2020-12-20")=0 
AND flight.flight_num in
	(SELECT flight.flight_num 
	FROM flight, airport
	WHERE flight.arrival_airport = airport.airport_name and (arrival_airport = 'JFK' OR airport_city = 'JFK')); 

-- 2. See the flights status based on flight number, arrival/departure date.
-- This is implemented through the function SearchFlightThroughFlightNumberAuth()

-- @app.route('/SearchFlightThroughFlightNumberAuth', methods=['GET', 'POST'])
-- def SearchFlightThroughFlightNumberAuth():

SELECT *
FROM flight
WHERE flight_num = 296 AND datediff(flight.departure_time,"2021-01-01")=0 AND datediff(flight.arrival_time,"2021-01-01")=0;

-- -----------------------------------------------REGISTER---------------------------------------------------------------------------------
-- Customer Register

INSERT INTO customer VALUES('c1@nyu.edu','Jennie','1234','1','Century Av','Shanghai','China',12345678,'A12345','2020-01-01','China','2000-01-01');

-- Booking Agent Register
INSERT INTO booking_agent VALUES('ba1@nyu.edu','1234',10);

-- Airline Staff Register
INSERT INTO airline_staff VALUES('as1','1234','Jennie','Shen','2000-01-01','Jet Blue');

-- ----------------------------------------------- LOGIN-----------------------------------------------------------------------------------
-- Customer Login
-- This is implemented through the function CustomerLoginAuth():

-- @app.route('/CustomerLoginAuth', methods=['GET', 'POST'])
-- def CustomerLoginAuth():
SELECT * 
FROM customer 
WHERE email = 'Customer@nyu.edu' and password = md5("abcd1234");

-- Booking Agent Login
-- This is implemented through the function AgentLoginAuth():

-- @app.route('/AgentLoginAuth', methods=['GET', 'POST'])
-- def AgentLoginAuth():

SELECT * 
FROM booking_agent 
WHERE email = 'Booking@agent.com' and password = md5('abcd1234');

-- Airline Staff Login
-- This is implemented through the function StaffLoginAuth():

-- @app.route('/StaffLoginAuth', methods=['GET', 'POST'])
-- def StaffLoginAuth():
SELECT * 
FROM airline_staff 
WHERE username = 'AirlineStaff' and password = md5('abcd1234');


-- ------------------------------------------------CUSTOMER FUNCTION-----------------------------------------------------------------------------------
-- 4. View flight information which he/she purchased.
--  This is implemented through the function CustomerViewMyFlights():

-- @app.route('/CustomerViewMyFlights', methods=['GET', 'POST'])
-- def CustomerViewMyFlights():

select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id
from purchases, ticket, flight, airport
where  purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.departure_airport = airport.airport_name
and purchases.customer_email = "Customer@nyu.edu"AND flight.departure_time >= "2020-12-19" AND flight.arrival_time <= "2020-12-22" and (flight.departure_airport = 'SFO' OR airport.airport_city = 'SFO')
AND (flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id) IN
(select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id
from purchases, ticket, flight, airport
where  purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.airport_name and
	purchases.customer_email = "Customer@nyu.edu" AND (flight.departure_time >=  "2020-12-19" AND flight.arrival_time <= "2020-12-22" )
    AND (flight.arrival_airport = "JFK" OR airport.airport_city = "JFK"));

-- default: showing for the upcoming flights
SELECT flight.airline_name,flight.flight_num,flight.departure_airport,flight.departure_time,flight.arrival_airport,flight.arrival_time,flight.price,flight.status,flight.airplane_id 
FROM purchases, ticket, flight  
WHERE purchases.ticket_id = ticket.ticket_id and flight.flight_num = ticket.flight_num and customer_email = 'Customer@nyu.edu';

-- 5. Customer purchases flight
-- This is implemented through the function CustomerPurchaseTickets():

-- @app.route('/CustomerPurchaseTickets', methods=['GET', 'POST'])
-- def CustomerPurchaseTickets():

-- query the total number of seats
select seats 
from flight, airplane 
where flight.airline_name = 'Jet Blue' and flight.flight_num = 139 and flight.airplane_id = airplane.airplane_id;

-- query the total number of tickets already sold
SELECT COUNT(ticket_id),flight.flight_num 
FROM ticket,flight WHERE flight.airline_name = 'Jet Blue' and flight.flight_num = 139 and ticket.flight_num = flight.flight_num;

-- query the new id
SELECT MAX(ticket_id) + 1 
FROM ticket;

-- purchase a new ticket
INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES (10, 'Jet Blue', 139);
INSERT INTO purchases (ticket_id, customer_email, booking_agent_id, purchase_date) VALUES (10, "Customer@nyu.edu",null, curdate());

-- 6. Search for flights

-- through date
-- This is impelmented through the function CustomerSearchFlightThroughDateAuth():

-- @app.route('/CustomerSearchFlightThroughDateAuth', methods=['GET', 'POST'])
-- def CustomerSearchFlightThroughDateAuth():

SELECT *
FROM flight, airport
WHERE flight.departure_airport = airport.airport_name and (departure_airport = "SFO" OR airport_city = "SFO") AND
datediff(flight.departure_time, "2020-12-20")=0
AND flight.flight_num in
(SELECT flight.flight_num 
FROM flight, airport
WHERE flight.arrival_airport = airport.airport_name and (arrival_airport = "JFK" OR airport_city = "JFK"));

-- through flight number
-- This is impelmented through the function CustomerSearchFlightThroughFlightNumberAuth():

-- @app.route('/CustomerSearchFlightThroughFlightNumberAuth', methods=['GET', 'POST'])
-- def CustomerSearchFlightThroughFlightNumberAuth():

SELECT *
FROM flight
WHERE flight_num = 139 AND datediff(flight.departure_time, "2020-12-20" )=0 AND datediff(flight.arrival_time, "2020-12-21" )=0;
                
-- 7. track my spending
-- This is implemented through the function CustomerTrackMySpending():

-- @app.route('/CustomerTrackMySpending', methods=['GET', 'POST'])
-- def CustomerTrackMySpending():

-- month wise money spent for last 6 months
select sum(flight.price), YEAR(purchase_date), MONTH(purchase_date)
from purchases, ticket, flight
where purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND purchases.customer_email = "Customer@nyu.edu" AND purchase_date > "2020-09" AND purchase_date < "2020-12"
group by YEAR(purchase_date), MONTH(purchase_date)
order by YEAR(purchase_date), MONTH(purchase_date);

-- total amount of money spent in the past year 
select sum(flight.price)
from purchases, ticket, flight
where purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND purchases.customer_email = "Customer@nyu.edu" AND purchase_date > date_sub(now(),INTERVAL 12 MONTH) AND purchase_date < now();

-- ------------------------------------------------BOOKING AGENT FUNCTION-----------------------------------------------------------------------------------
-- 4. View My flights:  Provide various ways for the booking agents to see flights information for which he/she purchased on behalf of customers.
-- This is implemeneted through BookingAgentViewMyFlights():

-- @app.route('/BookingAgentViewMyFlights', methods=['GET', 'POST'])
-- def BookingAgentViewMyFlights():

select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id, purchases.customer_email
from purchases, ticket, flight, airport, booking_agent
where booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.departure_airport = airport.airport_name
	and booking_agent.email = "Booking@agent.com" AND (flight.departure_time >= "2020-12-19" AND flight.arrival_time <= "2020-12-21") AND (flight.departure_airport = "La Guardia" OR airport.airport_city = "La Guardia" )
AND (flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id, purchases.customer_email) IN
(select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id, purchases.customer_email
from purchases, ticket, flight, airport, booking_agent
where booking_agent.booking_agent_id = purchases.booking_agent_id AND  purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.airport_name and
	booking_agent.email = "Booking@agent.com"  AND (flight.departure_time >= "2020-12-19" AND flight.arrival_time <= "2020-12-21")  AND (flight.arrival_airport = "SFO" OR airport.airport_city = "SFO"));

-- view my flights default query, see all the upcoming fight
select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id
from flight, ticket, purchases, booking_agent
where status = "upcoming" and flight.flight_num = ticket.flight_num and flight.airline_name = ticket.airline_name and purchases.ticket_id = ticket.ticket_id and purchases.booking_agent_id = booking_agent.booking_agent_id and booking_agent.email = "Booking@agent.com" ;

-- 5. Purchase tickets
-- This is implemented through the function BookingAgentPurchaseTickets():

-- @app.route('/BookingAgentPurchaseTickets', methods=['GET', 'POST'])
-- def BookingAgentPurchaseTickets():

-- query the total number of seats
select seats 
from flight, airplane 
where flight.airline_name = 'Jet Blue' and flight.flight_num = 139 and flight.airplane_id = airplane.airplane_id;

-- query the total number of tickets already sold
SELECT COUNT(ticket_id),flight.flight_num 
FROM ticket,flight WHERE flight.airline_name = 'Jet Blue' and flight.flight_num = 139 and ticket.flight_num = flight.flight_num;

-- query the new id
SELECT MAX(ticket_id) + 1 
FROM ticket;

-- purchase a new ticket
INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES (11, 'Jet Blue', 139);
INSERT INTO purchases (ticket_id, customer_email, booking_agent_id, purchase_date) VALUES (11, "Customer@nyu.edu",1, curdate());

-- 6. Search for flights
-- through date
-- This is implemeneted through BookingAgentSearchTicketsThroughDateAuth():

-- @app.route('/BookingAgentSearchTicketsThroughDateAuth', methods=['GET', 'POST'])
-- def BookingAgentSearchTicketsThroughDateAuth():
SELECT *
FROM flight, airport
WHERE flight.departure_airport = airport.airport_name and (departure_airport = "SFO" OR airport_city = "SFO") AND
datediff(flight.departure_time, "2020-12-20")=0
AND flight.flight_num in
(SELECT flight.flight_num 
FROM flight, airport
WHERE flight.arrival_airport = airport.airport_name and (arrival_airport = "JFK" OR airport_city = "JFK"));

-- through flight number
-- This is implemented through BookingAgentSearchTicketsThroughFlightNumberAuth():

-- @app.route('/BookingAgentSearchTicketsThroughFlightNumberAuth', methods=['GET', 'POST'])
-- def BookingAgentSearchTicketsThroughFlightNumberAuth():

SELECT *
FROM flight
WHERE flight_num = 139 AND datediff(flight.departure_time, "2020-12-20" )=0 AND datediff(flight.arrival_time, "2020-12-21" )=0;
   
-- 7. View my commission
-- This is implemented through the function BookingAgentViewMyCommission():

-- @app.route('/BookingAgentViewMyCommission', methods=['GET', 'POST'])
-- def BookingAgentViewMyCommission():

select sum(price * 0.1), avg(price * 0.1), count(*)
from flight, ticket, purchases, booking_agent
where booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND booking_agent.email = "Booking@agent.com" 
	AND purchase_date <= now() and purchase_date >= date_sub(now(),INTERVAL 1 MONTH);

-- View Top Customers
-- This is implemented through BookingAgentViewTopCustomers()

-- @app.route('/BookingAgentViewTopCustomers', methods = ["GET", "POST"])
-- def BookingAgentViewTopCustomers():

-- based on number of tickets
select customer_email, count(ticket_id) as count
from purchases, booking_agent
where purchase_date >= date_sub(now(),INTERVAL 6 MONTH) and booking_agent.booking_agent_id = purchases.booking_agent_id and booking_agent.email = "Booking@agent.com"
group by customer_email 
ORDER BY count DESC
limit 5;

-- based on commission
select customer_email, sum(price*0.1) as sum
from purchases, ticket, flight, booking_agent
where purchase_date >= date_sub(now(),INTERVAL 12 MONTH) and purchases.ticket_id = ticket.ticket_id and ticket.airline_name=flight.airline_name and ticket.flight_num = flight.flight_num
	and booking_agent.booking_agent_id = purchases.booking_agent_id and booking_agent.email = "Booking@agent.com"
group by customer_email
ORDER BY sum DESC
limit 5;
-- ---------------------------------------AIRLINE STAFF FUNCTION-----------------------------------------------------------------------------------
-- view my flights
-- This is implemented through StaffViewMyFlights():

-- @app.route('/StaffViewMyFlights', methods=['GET', 'POST'])
-- def StaffViewMyFlights():

--  Defaults will be showing all the upcoming flights operated by the airline he/she works for the next 30 days. 
select *
from flight
where airline_name = "Jet Blue" and status = "Upcoming" and departure_time <=  date_add(now(),INTERVAL 30 DAY);

--  He/she will be able to see all the customers of a particular flight.
select purchases.customer_email, customer.name
from flight, ticket, purchases, customer
where flight.flight_num = ticket.flight_num and flight.airline_name = "Jet Blue" and flight.airline_name = ticket.airline_name 
	and purchases.ticket_id = ticket.ticket_id and flight.flight_num = 915 and customer.email = purchases.customer_email;

-- search based range of dates, source/destination airports/city etc.
select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id
from flight, airport
where flight.airline_name = "Jet Blue" AND flight.departure_airport = airport.airport_name AND (flight.departure_airport = "SFO" OR airport.airport_city = "SFO")  AND flight.departure_time >= "2020-12-19"
AND flight.arrival_time <='2020-12-22'
AND (flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id) IN
(select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id
from flight, airport
where flight.airline_name = "Jet Blue" AND flight.departure_airport = airport.airport_name  AND (flight.arrival_airport = "JFK" OR airport.airport_city = "JFK") AND flight.departure_time >= "2020-12-19"
AND flight.arrival_time <='2020-12-22');

-- 5. create new flights 
-- This is implemented through the function StaffCreateNewFlights():

-- @app.route('/StaffCreateNewFlights', methods=['GET', 'POST'])
-- def StaffCreateNewFlights():

insert into flight values ("Jet Blue", 120, "SFO","2020-12-02 22:50:00", "JFK", "2020-12-03 08:50:00", 200, "Upcoming",1);
    
-- 6. change status of flights  
-- This is implemented through StaffChangeStatusofFlights():

-- @app.route('/StaffChangeStatusofFlights', methods=['GET', 'POST'])
-- def StaffChangeStatusofFlights():

update flight
set 
	status = "Delayed"
where 
	flight_num = 120 and airline_name = "Jet Blue";

-- 7. Add airplane in the system  
-- this is implemented through the function StaffAddAirplane()

-- @app.route('/StaffAddAirplane', methods = ['GET','POST'])
-- def StaffAddAirplane():

insert into airplane values ("Jet Blue", 4, 150); 
-- In the confirmation page, she/he will be able to see all the airplanes owned by the airline he/she works for.
select *
from airplane 
where airline_name = "Jet Blue";

-- 8. add new airport in the system 
-- this is implemented through StaffAddNewAirport():

-- @app.route('/StaffAddNewAirport', methods=['GET', 'POST'])
-- def StaffAddNewAirport():

insert into airport values("PVG","Shanghai");

-- 9.view all the booking agents 
-- this is implemented through the function StaffViewBookingAgent():

-- @app.route('/StaffViewBookingAgent', methods = ['GET','POST'])
-- def StaffViewBookingAgent():

-- based on the amount of commission
select booking_agent.email, purchases.booking_agent_id, sum(flight.price * 0.1) as commission
			from purchases,ticket, flight, booking_agent
			where booking_agent.booking_agent_id = purchases.booking_agent_id AND flight.airline_name  = "Jet Blue" AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND 
			purchases.ticket_id = ticket.ticket_id and purchases.purchase_date >= date_sub(now(),INTERVAL 12 MONTH) and purchases.booking_agent_id is not null 
            group by booking_agent.email
			ORDER BY commission DESC
			limit 5;
-- top 5 based on ticket sale
select booking_agent.email, purchases.booking_agent_id, count(purchases.ticket_id) AS count
				from purchases,ticket, booking_agent
				where ticket.airline_name  = "Jet Blue" AND booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id and purchases.purchase_date >= date_sub(now(),INTERVAL 1 MONTH) and purchases.booking_agent_id is not null
				group by booking_agent.email
				ORDER BY count DESC
				limit 5;
                
-- 10. View frequent customers
-- this is implemented through StaffViewFrequentCustomers():

-- @app.route('/StaffViewFrequentCustomers', methods = ['GET','POST'])
-- def StaffViewFrequentCustomers():

select customer.email, customer.name, count(purchases.ticket_id) as count
from purchases,ticket, customer
where ticket.airline_name = "Jet Blue" AND purchases.ticket_id = ticket.ticket_id and customer.email = purchases.customer_email and purchases.purchase_date >= date_sub(now(),INTERVAL 12 MONTH)
group by customer.email
ORDER BY count DESC
limit 1;

--  In addition, Airline Staff will be able to see a list of all flights a particular Customer has taken only on that particular airline.
select flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id
from purchases, ticket, flight
where purchases.ticket_id = ticket.ticket_id AND flight.flight_num = ticket.flight_num AND flight.airline_name = ticket.airline_name AND flight.airline_name = "Jet Blue" AND purchases.customer_email = "Customer@nyu.edu";

-- 11. View reports
-- this is implemented through the function StaffReports():

-- @app.route('/StaffReports', methods = ['GET','POST'])
-- def StaffReports():

select count(purchases.ticket_id),YEAR(purchase_date),MONTH(purchase_date)
from purchases, flight, ticket
where purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name and ticket.flight_num = flight.flight_num and flight.airline_name = "Jet Blue" and purchase_date >= "2019-01-01" and purchase_date <= "2021-01-01"
group by YEAR(purchase_date),MONTH(purchase_date);

-- 12. Comparison of Revenue earned
-- this is implemented through the function StaffComparisonOfRevenueEarned():

-- @app.route('/StaffComparisonOfRevenueEarned', methods = ['GET','POST'])
-- def StaffComparisonOfRevenueEarned():

select sum(flight.price)
from purchases,ticket, flight
where flight.airline_name  = "Jet Blue" AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND 
	purchases.ticket_id = ticket.ticket_id and purchases.purchase_date >= date_sub(now(),INTERVAL 12 MONTH) AND purchases.booking_agent_id is not null ;

-- 13. View Top destinations
-- this is implemented through StaffViewTopDestinations():

-- @app.route('/StaffViewTopDestinations', methods = ['GET','POST'])
-- def StaffViewTopDestinations():

select airport.airport_city, count(ticket.ticket_id) as count 
from purchases,ticket, flight, airport
where flight.airline_name  = "Jet Blue" AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.airport_name AND 
	purchases.ticket_id = ticket.ticket_id AND purchase_date >= date_sub(now(),INTERVAL 12 MONTH)
group by airport.airport_city
ORDER BY count DESC
limit 5;

    
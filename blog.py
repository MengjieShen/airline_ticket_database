from flask import Flask, render_template, request, url_for, redirect, session, jsonify
# import mysql.connector
import pymysql
import hashlib
import time
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Initialize the app from Flask
app = Flask(__name__,
			static_url_path="/",
			static_folder="static")

# Configure MySQL
# conn = mysql.connector.connect(host='localhost',
# 							   user='root',
# 							   password='12345678',
# 							   database='Airline')
conn = pymysql.connect(host='localhost',
							   user='root',
							   password='12345678',
							   database='Airline')

#Define a route to hello function
@app.route('/')
def hello():
	if 'username1' in session:
	    return redirect('/CustomerViewMyFlights') #这边要改
	elif 'username2' in session:
		return redirect('/BookingAgentViewMyFlights')
	elif 'username3' in session:
		return redirect('/StaffViewMyFlights')
	else:
		return render_template('index.html')

# Define route for home
@app.route('/index')
def index():
    return render_template('index.html')

# Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

# Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

# -------------------------------------------------Public Function --------------------------------------------

# Search Flight Page thorugh date
@app.route('/SearchFlightThroughDateAuth', methods=['GET', 'POST'])
def SearchFlightThroughDateAuth():
	date = request.form['date']
	departure = request.form['departure']
	arrival = request.form['arrival']
	cursor = conn.cursor()
	query = """SELECT *\
			FROM flight, airport\
			WHERE flight.departure_airport = airport.airport_name and (departure_airport = %s OR airport_city = %s) AND\
			datediff(flight.departure_time, %s)=0\
			AND flight.flight_num in\
			(SELECT flight.flight_num \
			FROM flight, airport\
			WHERE flight.arrival_airport = airport.airport_name and (arrival_airport = %s OR airport_city = %s))"""
	cursor.execute(query, (departure, departure, date, arrival, arrival))
	rows = cursor.fetchall()
	print("Show the info", rows)
	cursor.close()
	return render_template('PublicFlightInfo.html', rows=rows)

# Search Flight Status through flight number
@app.route('/SearchFlightThroughFlightNumberAuth', methods=['GET', 'POST'])
def SearchFlightThroughFlightNumberAuth():
	FlightNumber = request.form['FlightNumber']
	DepartureDate = request.form['DepartureDate']
	ArrivalDate = request.form['ArrivalDate']

	cursor = conn.cursor()

	query = "SELECT *\
			FROM flight\
			WHERE flight_num = {} AND datediff(flight.departure_time, '{}')=0 AND datediff(flight.arrival_time, '{}')=0"
	cursor.execute(query.format(FlightNumber,DepartureDate,ArrivalDate))
	rows = cursor.fetchall()
	cursor.close()
	return render_template('PublicFlightInfo.html', rows=rows)

# ----------------------------------------Login-----------------------------------------------
# Authenticates the login-Customer
@app.route('/CustomerLoginAuth', methods=['GET', 'POST'])
def CustomerLoginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM customer WHERE email = '{}' and password = '{}'"
	cursor.execute(query.format(email, hashlib.md5(password.encode()).hexdigest()))
	#stores the results in a variable
	data = cursor.fetchone()
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username1'] = email
		#data = # fetch info from the data base where id = login customer id
		return redirect("/CustomerViewMyFlights")
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=True)


# Authenticates the login-Booking Agent
@app.route('/AgentLoginAuth', methods=['GET', 'POST'])
def AgentLoginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM booking_agent WHERE email = '{}' and password = '{}'"
	cursor.execute(query.format(email, hashlib.md5(password.encode()).hexdigest()))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username2'] = email
		return redirect("/BookingAgentViewMyFlights")
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=True)


# Authenticates the login-Staff
@app.route('/StaffLoginAuth', methods=['GET', 'POST'])
def StaffLoginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM airline_staff WHERE username = '{}' and password = '{}'"
	cursor.execute(query.format(username, hashlib.md5(password.encode()).hexdigest()))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username3'] = [username,data[-1]]
		# airline = session['username'][1]
		# status = "Upcoming"
		# new_query = "select *\
		# 		from flight\
		# 		where airline_name = '{}'  and status = '{}' and departure_time <=  date_add(now(),INTERVAL 30 DAY)"
		# cursor.execute(new_query.format(airline, status))
		# rows = cursor.fetchall()
		# cursor.close()
		return redirect('/StaffViewMyFlights')
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=True)


# -------------------------------------Register---------------------------------------------------------
# Authenticates the register for customer
@app.route('/CustomerRegisterAuth', methods=['GET', 'POST'])
def CustomerRegisterAuth():
	#grabs information from the forms
	email = request.form['email']
	name = request.form['name']
	password = request.form['password']
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_number = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country =request.form['passport_country']
	date_of_birth =request.form['date_of_birth']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM customer WHERE email = '{}'"
	cursor.execute(query.format(email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists."
		return render_template('register.html', error = error)
	else:
		try:
			ins = "INSERT INTO customer VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
			cursor.execute(ins.format(email, name, hashlib.md5(password.encode()).hexdigest(), building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
			conn.commit()
			cursor.close()
		except:
			return render_template('register.html', error='Failed to register user.')
		return redirect('/login')

# Authenticates the register for booking agent
@app.route('/AgentRegisterAuth', methods=['GET', 'POST'])  # 跟tina的表单名要一样！！！
def AgentRegisterAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM booking_agent WHERE email = '{}'"
	cursor.execute(query.format(email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = "INSERT INTO booking_agent VALUES('{}','{}','{}')"
		cursor.execute(ins.format(email, hashlib.md5(password.encode()).hexdigest(), booking_agent_id))
		conn.commit()
		cursor.close()
		return redirect('/login')

# Authenticates the register for airline staff
@app.route('/AirlineStaffRegisterAuth', methods=['GET', 'POST'])
def AirlineStaffRegisterAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	airline_name = request.form['airline_name']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM airline_staff WHERE username = '{}'"
	cursor.execute(query.format(username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = True)
	else:
		try:
			ins = "INSERT INTO airline_staff VALUES('{}','{}','{}','{}','{}','{}')"
			cursor.execute(ins.format(username, hashlib.md5(password.encode()).hexdigest(), first_name, last_name, date_of_birth, airline_name))
			conn.commit()
			cursor.close()
			return render_template('login.html', message = True)
		except:
			return render_template('register.html', error = True)


# --------------------------------------------------------Log out--------------------------------------------
@app.route('/CustomerLogout')
def CustomerLogout():
	session.pop('username1')
	return redirect('/')
@app.route('/BookingAgentLogout')
def BookingAgentLogout():
	session.pop('username2')
	return redirect('/')
@app.route('/AirlineStaffLogout')
def AirlineStaffLogout():
	session.pop('username3')
	return redirect('/')
#--------------------------------------------------------Customer Function----------------------------------------------
# Customer view their booked flights
@app.route('/CustomerViewMyFlights', methods=['GET', 'POST'])
def CustomerViewMyFlights():
	if session.get('username1'):
		email = session['username1']
		cursor = conn.cursor()
		if request.method == 'POST':
			departure = request.form['departure']
			destination = request.form['destination']
			DepartureDate = request.form['DepartureDate']
			ArrivalDate = request.form['ArrivalDate']
			para_dept = [email]
			para_arr = [email]
			query_dept = "select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
					from purchases, ticket, flight, airport\
					where  purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.departure_airport = airport.airport_name and purchases.customer_email = '{}' "
			query_arr = "AND (flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id) IN\
					(select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
					from purchases, ticket, flight, airport\
					where  purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.airport_name and purchases.customer_email = '{}' "
			if departure != "":
				query_dept += " AND (flight.departure_airport = '{}' OR airport.airport_city = '{}')"
				para_dept.append(pymysql.escape_string(departure))
				para_dept.append(pymysql.escape_string(departure))
			if destination != "":
				query_arr += " AND (flight.arrival_airport = '{}' OR airport.airport_city = '{}')"
				para_arr.append(pymysql.escape_string(destination))
				para_arr.append(pymysql.escape_string(destination))
			if DepartureDate != "":
				query_dept += " AND flight.departure_time >= '{}'"
				query_arr += " AND flight.departure_time >= '{}'"
				para_arr.append(DepartureDate)
				para_dept.append(DepartureDate)
			if ArrivalDate != "":
				query_dept += " AND flight.arrival_time <= '{}'"
				query_arr += " AND flight.arrival_time <= '{}'"
				para_arr.append(ArrivalDate)
				para_dept.append(ArrivalDate)
			query = query_dept +query_arr + ")"
			para = para_dept + para_arr
			cursor.execute(query.format(*para))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('CustomerViewMyFlights.html', rows=rows,message=True)
		elif request.method == 'GET':
			new_query = "SELECT flight.airline_name,flight.flight_num,flight.departure_airport,flight.departure_time,flight.arrival_airport,flight.arrival_time,flight.price,flight.status,flight.airplane_id FROM purchases, ticket, flight  WHERE purchases.ticket_id = ticket.ticket_id and flight.flight_num = ticket.flight_num and customer_email = '{}'"
			cursor.execute(new_query.format(email))
			rows = cursor.fetchall()
			return render_template('CustomerViewMyFlights.html', rows=rows)
	else:
		return redirect('/login')

@app.route('/CustomerSearchTickets')
def customerSearchTickets():
	if session.get('username1'):
		return render_template('CustomerSearchTickets.html')
	else:
		return redirect('/login')

# Customer purchase new tickets
@app.route('/CustomerPurchaseTickets', methods=['GET', 'POST'])
def CustomerPurchaseTickets():
	if session.get('username1'):
		email = session['username1']
		if request.method == "GET":
			return render_template("CustomerSearchTickets.html")
		else:
			try:
				# cursor used to send queries
				cursor = conn.cursor()
				AirlineCompany = request.form['AirlineCompany']
				FlightNumber = request.form['FlightNumber']
				# executes query
				query_seats_total = "select seats from flight, airplane where flight.airline_name = '{}' and flight.flight_num = {} and flight.airplane_id = airplane.airplane_id"
				cursor.execute(query_seats_total.format(AirlineCompany,FlightNumber))
				seats_total = cursor.fetchall()
				query_purchased = "SELECT COUNT(ticket_id),flight.flight_num FROM ticket,flight WHERE flight.airline_name = '{}' and flight.flight_num = {} and ticket.flight_num = flight.flight_num"
				cursor.execute(query_purchased.format(AirlineCompany, FlightNumber))
				purchased = cursor.fetchall()
				query_ticket_id = "SELECT MAX(ticket_id) + 1 FROM ticket;"
				cursor.execute(query_ticket_id)
				ticket_id = cursor.fetchall()
				ticket_id = ticket_id[0][0]
				# stores the results in a variable
			except:
				return render_template('CustomerSearchTickets.html', error=True)
			if seats_total == purchased:
				conn.commit()
				cursor.close()
				return render_template('CustomerSearchTickets.html',error = True)#记得修改错误信息
			else:
				try:
					query_insert_ticket = "INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES (\'{}\', \'{}\',\'{}\')"
					query_insert_purchase = "INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES (\'{}\', \'{}\',null, \'{}\')"
					t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
					t = t[:10]
					print(ticket_id, AirlineCompany, FlightNumber,email,t)
					cursor.execute(query_insert_ticket.format(ticket_id, AirlineCompany, FlightNumber))
					cursor.execute(query_insert_purchase.format(ticket_id,email,t))
					conn.commit()
					cursor.close()
					return render_template('CustomerSearchTickets.html',message = True)
				except:
					return render_template('CustomerSearchTickets.html',error = True)
	else:
		return redirect('/login')

# Customer Search Flight Page thorugh date
@app.route('/CustomerSearchFlightThroughDateAuth', methods=['GET', 'POST'])
def CustomerSearchFlightThroughDateAuth():
	date = request.form['date']
	departure = request.form['departure']
	arrival = request.form['arrival']
	cursor = conn.cursor()
	query = "SELECT *\
			FROM flight, airport\
			WHERE flight.departure_airport = airport.airport_name and (departure_airport = %s OR airport_city = %s) AND\
			datediff(flight.departure_time, %s)=0\
			AND flight.flight_num in\
			(SELECT flight.flight_num \
			FROM flight, airport\
			WHERE flight.arrival_airport = airport.airport_name and (arrival_airport = %s OR airport_city = %s))"
	cursor.execute(query, (departure, departure, date, arrival, arrival))
	rows = cursor.fetchall()
	cursor.close()
	return render_template('CustomerSearchTickets.html', rows=rows)

# Search Flight Status through flight number
@app.route('/CustomerSearchFlightThroughFlightNumberAuth', methods=['GET', 'POST'])
def CustomerSearchFlightThroughFlightNumberAuth():
	FlightNumber = request.form['FlightNumber']
	DepartureDate = request.form['DepartureDate']
	ArrivalDate = request.form['ArrivalDate']

	cursor = conn.cursor()

	query = "SELECT *\
				FROM flight\
				WHERE flight_num = %s AND datediff(flight.departure_time, %s )=0 AND datediff(flight.arrival_time, %s )=0"
	cursor.execute(query, (FlightNumber, DepartureDate, ArrivalDate))
	rows = cursor.fetchall()
	cursor.close()
	return render_template('CustomerSearchTickets.html', rows=rows)

@app.route('/CustomerTrackMySpending', methods=['GET', 'POST'])
def CustomerTrackMySpending():
	if session.get('username1'):
		if request.method == 'GET':
			return render_template("CustomerTrackMySpending.html")
		email = session['username1']
		cursor = conn.cursor()
		if request.form.get('StartMonth') is None:
			StartMonth_1 = str(date.today()- relativedelta(months = 12))
			StartMonth = str(date.today()- relativedelta(months = 6))
			EndMonth = str(date.today())
		else:
			StartMonth_1 = request.form['StartMonth']
			StartMonth = request.form['StartMonth']
			EndMonth = request.form['EndMonth']
		query_1 = "select sum(flight.price)\
					from purchases, ticket, flight\
					where purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND purchases.customer_email = '{}' AND purchase_date >= '{}' AND purchase_date <= '{}'"
		query = "select sum(flight.price), YEAR(purchase_date), MONTH(purchase_date)\
				from purchases, ticket, flight\
				where purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND purchases.customer_email = '{}' AND purchase_date >= '{}' AND purchase_date <= '{}'\
				group by YEAR(purchase_date), MONTH(purchase_date);"
		cursor.execute(query_1.format(email,StartMonth_1, EndMonth))
		result_1 = cursor.fetchone()
		result_1 = int(result_1[0]) if result_1[0] else 0
		cursor.execute(query.format(email, StartMonth, EndMonth))
		result = cursor.fetchall()
		rows = {}
		startDate = datetime.strptime(StartMonth,'%Y-%m-%d')
		endDate = datetime.strptime(EndMonth, '%Y-%m-%d')
		year = startDate.year
		month = startDate.month
		while year <= endDate.year:
			if year == endDate.year and month == endDate.month+1:
				break
			if month <= 12:
				temp = str(year)+"-"+str(month)
				rows[temp] = 0
				month += 1
			else:
				year += 1
				month = 1
		for i in result:
			rows[str(i[1])+"-"+str(i[2])] = int(i[0])
		array_1 = []
		for (key,value) in rows.items():
			array_1.append([key, value])
		cursor.close()
		dic = {}
		dic["data1"] = result_1
		dic["data2"] = array_1
		return jsonify(dic)
	else:
		return redirect ('/login')

# ------------------------------------------------------Booking agent Function----------------------------------------------
@app.route('/BookingAgentViewMyFlights', methods=['GET', 'POST'])
def BookingAgentViewMyFlights():
	if session.get('username2'):
		email = session['username2']
		if request.method == 'GET':
			cursor = conn.cursor()
			query = "select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
					from flight, ticket, purchases, booking_agent\
					where status = 'upcoming' and flight.flight_num = ticket.flight_num and flight.airline_name = ticket.airline_name and purchases.ticket_id = ticket.ticket_id and purchases.booking_agent_id = booking_agent.booking_agent_id and booking_agent.email = '{}';"
			cursor.execute(query.format(email))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('BookingAgentViewMyFlights.html', rows = rows)
		if request.method == 'POST':
			cursor = conn.cursor()
			departure = request.form['departure']
			destination = request.form['destination']
			DepartureDate = request.form['DepartureDate']
			ArrivalDate = request.form['ArrivalDate']
			para_dept = [email]
			para_arr = [email]
			query_dept = "select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
					from purchases, ticket, flight, airport, booking_agent\
					where booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.departure_airport = airport.airport_name and booking_agent.email = '{}' "
			query_arr = "AND (flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id) IN\
					(select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
					from purchases, ticket, flight, airport, booking_agent\
					where booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.airport_name and booking_agent.email = '{}' "
			if departure != "":
				query_dept += " AND (flight.departure_airport = '{}' OR airport.airport_city = '{}')"
				para_dept.append(pymysql.escape_string(departure))
				para_dept.append(pymysql.escape_string(departure))
			if destination != "":
				query_arr += " AND (flight.arrival_airport = '{}' OR airport.airport_city = '{}')"
				para_arr.append(pymysql.escape_string(destination))
				para_arr.append(pymysql.escape_string(destination))
			if DepartureDate != "":
				query_dept += " AND flight.departure_time >= '{}'"
				query_arr += " AND flight.departure_time >= '{}'"
				para_arr.append(DepartureDate)
				para_dept.append(DepartureDate)
			if ArrivalDate != "":
				query_dept += " AND flight.arrival_time <='{}'"
				query_arr += " AND flight.arrival_time <= '{}'"
				para_arr.append(ArrivalDate)
				para_dept.append(ArrivalDate)
			query = query_dept +query_arr + ")"
			para = para_dept + para_arr
			cursor.execute(query.format(*para))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('BookingAgentViewMyFlights.html', rows=rows)
	else:
		return redirect('/login')

@app.route('/BookingAgentSearchTickets')
def BookingAgentSearchTickets():
	if session.get('username2'):
		return render_template('BookingAgentSearchTickets.html')
	else:
		return redirect('/login')

# search flight for booking agent
@app.route('/BookingAgentSearchTicketsThroughDateAuth', methods=['GET', 'POST'])
def BookingAgentSearchTicketsThroughDateAuth():
	date = request.form['date']
	departure = request.form['departure']
	arrival = request.form['arrival']
	cursor = conn.cursor()
	query = "SELECT *\
			FROM flight, airport\
			WHERE flight.departure_airport = airport.airport_name and (departure_airport = %s OR airport_city = %s) AND\
			datediff(flight.departure_time, %s)=0\
			AND flight.flight_num in\
			(SELECT flight.flight_num \
			FROM flight, airport\
			WHERE flight.arrival_airport = airport.airport_name and (arrival_airport = %s OR airport_city = %s))"
	cursor.execute(query, (departure, departure, date, arrival, arrival))
	rows = cursor.fetchall()
	cursor.close()
	return render_template('BookingAgentSearchTickets.html', rows=rows)

@app.route('/BookingAgentSearchTicketsThroughFlightNumberAuth', methods=['GET', 'POST'])
def BookingAgentSearchTicketsThroughFlightNumberAuth():
	FlightNumber = request.form['FlightNumber']
	DepartureDate = request.form['DepartureDate']
	ArrivalDate = request.form['ArrivalDate']

	cursor = conn.cursor()

	query = "SELECT *\
				FROM flight\
				WHERE flight_num = %s AND datediff(flight.departure_time, %s)=0 AND datediff(flight.arrival_time, %s)=0"
	cursor.execute(query, (FlightNumber, DepartureDate, ArrivalDate))
	rows = cursor.fetchall()
	cursor.close()
	return render_template('BookingAgentSearchTickets.html', rows=rows)

# Booking Agent purchase new tickets
@app.route('/BookingAgentPurchaseTickets', methods=['GET', 'POST'])
def BookingAgentPurchaseTickets():
	if session.get('username2'):
		if request.method == "POST":
			try:
				email = session['username2']
				# cursor used to send queries
				cursor = conn.cursor()
				customer_email = request.form['customer_email']
				AirlineCompany = request.form['AirlineCompany']
				FlightNumber = request.form['FlightNumber']
				# executes query
				query_seats_total = "select seats from flight, airplane where flight.airline_name = '{}' and flight.flight_num = {} and flight.airplane_id = airplane.airplane_id"
				cursor.execute(query_seats_total.format(AirlineCompany,FlightNumber))
				seats_total = cursor.fetchall()
				query_purchased = "SELECT COUNT(ticket_id),flight.flight_num FROM ticket,flight WHERE flight.airline_name = '{}' and flight.flight_num = {} and ticket.flight_num = flight.flight_num"
				cursor.execute(query_purchased.format(AirlineCompany, FlightNumber))
				purchased = cursor.fetchall()
				query_ticket_id = "SELECT MAX(ticket_id) + 1 FROM ticket"
				cursor.execute(query_ticket_id)
				ticket_id = cursor.fetchall()
				ticket_id = ticket_id[0][0]
				booking_agent_id_query = "SELECT booking_agent_id FROM booking_agent WHERE email = '{}'"
				cursor.execute(booking_agent_id_query.format(email))
				booking_agent_id = cursor.fetchall()
				booking_agent_id = booking_agent_id[0][0]
			except:
				return render_template('BookingAgentSearchTickets.html', error = True)
			# stores the results in a variable
			if seats_total == purchased:
				conn.commit()
				cursor.close()
				return render_template('BookingAgentSearchTickets.html',error = True)#记得修改错误信息
			else:
				try:
					query_insert_ticket = "INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES (\'{}\', \'{}\',\'{}\')"
					query_insert_purchase = "INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES (\'{}\', \'{}\',\'{}\', \'{}\')"
					t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
					t = t[:10]
					print(ticket_id, AirlineCompany, FlightNumber,customer_email,t)
					cursor.execute(query_insert_ticket.format(ticket_id, AirlineCompany, FlightNumber))
					cursor.execute(query_insert_purchase.format(ticket_id,customer_email,booking_agent_id,t))
					conn.commit()
					cursor.close()
					return render_template('BookingAgentSearchTickets.html',message = True)#要修改
				except:
					return render_template('BookingAgentSearchTickets.html', error = True)
		else:
			return render_template('BookingAgentSearchTickets.html')
	else:
		return redirect('/login')

@app.route('/BookingAgentViewMyCommission', methods=['GET', 'POST'])
def BookingAgentViewMyCommission():
	if session.get('username2'):
		username = session['username2']
		if request.method == 'GET':
			cursor = conn.cursor()
			DateAfter = str(date.today()- relativedelta(months = 6))
			DateBefore = str(date.today())
			query = "select sum(price * 0.1), avg(price * 0.1), count(*)\
				from flight, ticket, purchases, booking_agent\
				where booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num \
				AND booking_agent.email = '{}' AND purchase_date >= '{}' and purchase_date <= '{}'"
			cursor.execute(query.format(username, DateAfter, DateBefore))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('BookingAgentViewMyCommission.html', rows=rows)
		elif request.method == 'POST':
			DateAfter = request.form['DateAfter']
			DateBefore = request.form['DateBefore']
			cursor = conn.cursor()
			query = "select sum(price * 0.1), avg(price * 0.1), count(*)\
				from flight, ticket, purchases, booking_agent\
				where booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num \
				AND booking_agent.email = '{}' AND purchase_date >= '{}' and purchase_date <= '{}'"
			cursor.execute(query.format(username, DateAfter, DateBefore))
			rows = cursor.fetchall()
			cursor.close()
			return render_template('BookingAgentViewMyCommission.html', rows = rows)
	else:
		return redirect('/login')

@app.route('/BookingAgentViewTopCustomers', methods = ["GET", "POST"])
def BookingAgentViewTopCustomers():
	if session.get('username2'):
		username = session['username2']
		cursor = conn.cursor()
		query_1 = "select customer_email, count(ticket_id) as count\
			from purchases, booking_agent where purchase_date >= date_sub(now(),INTERVAL 6 MONTH) and booking_agent.booking_agent_id = purchases.booking_agent_id and booking_agent.email = '{}' \
			group by customer_email \
			ORDER BY count DESC\
			limit 5;"
		cursor.execute(query_1.format(username))
		rows1 = cursor.fetchall()
		query_2 = "select customer_email, sum(price*0.1) as sum\
					from purchases, ticket, flight, booking_agent\
					where purchase_date >= date_sub(now(),INTERVAL 12 MONTH) and purchases.ticket_id = ticket.ticket_id and ticket.airline_name=flight.airline_name and ticket.flight_num = flight.flight_num\
					and booking_agent.booking_agent_id = purchases.booking_agent_id and booking_agent.email = '{}'\
					group by customer_email\
					ORDER BY sum DESC\
					limit 5;"
		cursor.execute(query_2.format(username))
		rows2 = cursor.fetchall()
		cursor.close()

		# BEGIN
		my_array1 = "["
		for email, y in rows1:
			my_array1 += "{name: \"%s\", y: %s}," % (email, y)
		my_array1.rstrip(",")
		my_array1 += "]"

		my_array2 = "["
		for email, y in rows2:
			my_array2 += "{name: \"%s\", y: %s}," % (email, y)
		my_array2.rstrip(",")
		my_array2 += "]"
		# END
		return render_template("BookingAgentViewTopCustomers.html",my_array1 = my_array1, my_array2 = my_array2)
	else:
		return redirect('/login')

# -----------------------------------------------------Airline Staff Function-------------------------------------
@app.route('/StaffViewMyFlights', methods=['GET', 'POST'])
def StaffViewMyFlights():
	if session.get('username3'):
		if request.method == "GET":
			airline = session['username3'][1]
			status = "Upcoming"
			cursor = conn.cursor()
			query = "select *\
					from flight\
					where airline_name = %s  and status = %s and departure_time <=  date_add(now(),INTERVAL 30 DAY)"
			cursor.execute(query, (airline, status))

			rows1 = cursor.fetchall()
			cursor.close()

			return render_template('StaffViewMyFlights.html', rows1 = rows1)
	else:
		return redirect('/login')

@app.route('/StaffViewMyFlights_search', methods = ['GET', 'POST'])
def StaffViewMyFlights_search():
	username = session['username3'][1]
	cursor = conn.cursor()
	departure = request.form['departure']
	destination = request.form['destination']
	DepartureDate = request.form['DepartureDate']
	ArrivalDate = request.form['ArrivalDate']
	para_dept = [username]
	para_arr = [username]
	query_dept = "select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
			from flight, airport\
			where flight.airline_name = %s AND flight.departure_airport = airport.airport_name "
	query_arr = "AND (flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id) IN\
			(select flight.airline_name, flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
			from flight, airport\
			where flight.airline_name = %s AND flight.departure_airport = airport.airport_name "
	if departure != "":
		query_dept += " AND (flight.departure_airport = %s OR airport.airport_city = %s)"
		para_dept.append(pymysql.escape_string(departure))
		para_dept.append(pymysql.escape_string(departure))
	if destination != "":
		query_arr += " AND (flight.arrival_airport = %s OR airport.airport_city = %s)"
		para_arr.append(pymysql.escape_string(destination))
		para_arr.append(pymysql.escape_string(destination))
	if DepartureDate != "":
		query_dept += " AND flight.departure_time >= %s"
		query_arr += " AND flight.departure_time >= %s"
		para_arr.append(DepartureDate)
		para_dept.append(DepartureDate)
	if ArrivalDate != "":
		query_dept += " AND flight.arrival_time <='{}'"
		query_arr += " AND flight.arrival_time <= '{}'"
		para_arr.append(ArrivalDate)
		para_dept.append(ArrivalDate)
	query = query_dept +query_arr + ")"
	para = para_dept + para_arr
	cursor.execute(query, para)
	rows1 = cursor.fetchall()
	cursor.close()
	return render_template('StaffViewMyFlights.html', rows1 = rows1)

@app.route('/StaffViewMyFlights_flightNumber', methods =['GET', 'POST'])
def StaffViewMyFlights_flightNumber():
	airline = session['username3'][1]
	cursor = conn.cursor()
	status = "Upcoming"
	query_1 = "select *\
			from flight\
			where airline_name = %s  and status = %s and departure_time <=  date_add(now(),INTERVAL 30 DAY)"
	cursor.execute(query_1, (airline, status))
	rows1 = cursor.fetchall()
	flight_num = request.form['flight_number']
	query = "select purchases.customer_email, customer.name, customer.phone_number\
			from flight, ticket, purchases, customer\
			where flight.flight_num = ticket.flight_num and flight.airline_name = %s and flight.airline_name = ticket.airline_name \
			and purchases.ticket_id = ticket.ticket_id and flight.flight_num = %s and customer.email = purchases.customer_email;"
	cursor.execute(query, (airline, flight_num))
	rows2 = cursor.fetchall()
	cursor.close()
	return render_template("StaffViewMyFlights.html", rows1 = rows1, rows2 = rows2)

@app.route('/StaffCreateNewFlights', methods=['GET', 'POST'])
def StaffCreateNewFlights():
	if session.get('username3'):
		airline = session['username3'][1]
		# cursor used to send queries
		cursor = conn.cursor()
		# executes query
		query = "select * from flight where airline_name = '{}'"
		cursor.execute(query.format(airline))
		# stores the results in a variable
		rows = cursor.fetchall()
		cursor.close()
		if request.method == "GET":
			airline = session['username3'][1]
			# cursor used to send queries
			cursor = conn.cursor()
			# executes query
			query = "select * from flight where airline_name = '{}'"
			cursor.execute(query.format(airline))
			# stores the results in a variable
			rows = cursor.fetchall()
			cursor.close()
			return render_template('StaffCreateNewFlights.html',rows = rows)
		else:
			try:
				airline = session['username3'][1]
				cursor = conn.cursor()
				flight_num = request.form['flight_num']
				DepatureAirport = request.form['DepatureAirport']
				DepatureTime = request.form['DepatureTime']
				ArrivalAirport = request.form['ArrivalAirport']
				ArrivalTime = request.form['ArrivalTime']
				TicketPrice = request.form['TicketPrice']
				FlightStatus = request.form['FlightStatus']
				airplane_id = request.form['airplane_id']
				query = "insert into flight values ('{}', {}, '{}', '{}', '{}', '{}', {},'{}',{})"
				cursor.execute(query.format(airline, flight_num, pymysql.escape_string(DepatureAirport),DepatureTime, pymysql.escape_string(ArrivalAirport), ArrivalTime, TicketPrice, FlightStatus, airplane_id))
				conn.commit()
				cursor.close()
				return render_template("StaffCreateNewFlights.html", rows=rows, message=True)  # 加个成功的页面
			except:
				return render_template('StaffCreateNewFlights.html', rows = rows, error = True)


	else:
		return redirect('/login')

@app.route('/StaffChangeStatusofFlights', methods=['GET', 'POST'])
def StaffChangeStatusofFlights():
	if session.get('username3'):
		if request.method == "GET":
			return render_template('StaffChangeStatusofFlights.html')
		if request.method == "POST":
			airline = session['username3'][1]
			cursor = conn.cursor()
			flight_num = request.form['flight_num']
			status = request.form['status']
			query = "update flight\
					set status = '{}'\
					where flight_num = {} and airline_name = '{}'"
			try:
				cursor.execute(query.format(status, flight_num, airline))
				conn.commit()
				cursor.close()
				return render_template("StaffChangeStatusofFlights.html",message = True)
			except:
				return render_template("StaffChangeStatusofFlights.html",error = True)
	else:
		return redirect('/login')

@app.route('/StaffAddAirplane', methods = ['GET','POST'])
def StaffAddAirplane():
	if session.get('username3'):
		airline = session['username3'][1]
		# cursor used to send queries
		cursor = conn.cursor()
		# executes query
		query = "select * from airplane where airline_name = '{}'"
		cursor.execute(query.format(airline))
		# stores the results in a variable
		rows1 = cursor.fetchall()
		cursor.close()
		if request.method == "GET":
			return render_template('StaffAddAirplane.html',rows1 = rows1)
		else:
			airline = session['username3'][1]
			cursor = conn.cursor()
			airplane_id = request.form['airplane_id']
			seats = request.form['seats']
			query = "insert into airplane values ('{}', {}, {}); "
			try:
				cursor.execute(query.format(airline, airplane_id, seats))
				conn.commit()
				cursor.close()
				return render_template("StaffAddAirplane.html",rows1 = rows1,message = True)
			except:
				return render_template("StaffAddAirplane.html",rows1 = rows1,error = True)
	else:
		return redirect('/login')

@app.route('/StaffAddNewAirport', methods=['GET', 'POST'])
def StaffAddNewAirport():
	if request.method == 'POST':
		try:
			cursor = conn.cursor()
			airport_city = request.form['airport_city']
			airport_name = request.form['airport_name']
			query = "insert into airport values ('{}', '{}')"
			cursor.execute(query.format(pymysql.escape_string(airport_name),pymysql.escape_string(airport_city)))
			conn.commit()
			cursor.close()
			return render_template("StaffAddNewAirport.html",message = True)
		except:
			return render_template("StaffAddNewAirport.html",error = True)
	elif request.method == 'GET':
		return render_template("StaffAddNewAirport.html")

@app.route('/StaffViewFrequentCustomers', methods = ['GET','POST'])
def StaffViewFrequentCustomers():
	if session.get("username3"):
		if request.method == "POST":
			airline = session['username3'][1]
			cursor = conn.cursor()
			query = "select customer.email, customer.name, count(purchases.ticket_id) as count\
					from purchases,ticket, customer\
					where ticket.airline_name = '{}' AND purchases.ticket_id = ticket.ticket_id and customer.email = purchases.customer_email and purchases.purchase_date >= date_sub(now(),INTERVAL 12 MONTH)\
					group by customer.email\
					ORDER BY count DESC\
					limit 1;"
			cursor.execute(query.format(airline))
			rows1 = cursor.fetchall()
			email = request.form['email']
			query_2 = "select flight.flight_num, flight.departure_airport, flight.departure_time, flight.arrival_airport, flight.arrival_time, flight.price, flight.status, flight.airplane_id\
						from purchases, ticket, flight\
						where purchases.ticket_id = ticket.ticket_id AND flight.flight_num = ticket.flight_num AND flight.airline_name = ticket.airline_name AND flight.airline_name = '{}' AND purchases.customer_email = '{}'"
			cursor.execute(query_2.format(airline, email))
			rows2 = cursor.fetchall()
			cursor.close()
			return render_template("StaffViewFrequentCustomers.html", rows1= rows1, rows2=rows2)
		else:
			airline = session['username3'][1]
			cursor = conn.cursor()
			query = "select customer.email, customer.name, count(purchases.ticket_id) as count\
					from purchases,ticket, customer\
					where ticket.airline_name = '{}' AND purchases.ticket_id = ticket.ticket_id and customer.email = purchases.customer_email and purchases.purchase_date >= date_sub(now(),INTERVAL 12 MONTH)\
					group by customer.email\
					ORDER BY count DESC\
					limit 1;"
			cursor.execute(query.format(airline))
			rows1 = cursor.fetchall()
			cursor.close()
			return render_template("StaffViewFrequentCustomers.html", rows1 = rows1)
	else:
		return redirect('/login')

@app.route('/StaffViewBookingAgent', methods = ['GET','POST'])
def StaffViewBookingAgent():
	if session.get("username3"):
		airline = session['username3'][1]
		cursor = conn.cursor()
		query_1 = "select booking_agent.email, purchases.booking_agent_id, count(purchases.ticket_id) AS count\
					from purchases,ticket, booking_agent\
					where ticket.airline_name  = '{}' AND booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id and purchases.purchase_date >= date_sub(now(),INTERVAL 1 MONTH) and purchases.booking_agent_id is not null\
					group by booking_agent.email\
					ORDER BY count DESC\
					limit 5;"
		cursor.execute(query_1.format(airline))
		rows1 = cursor.fetchall()
		query_2 = "select booking_agent.email, purchases.booking_agent_id, count(purchases.ticket_id) AS count\
					from purchases,ticket, booking_agent\
					where  ticket.airline_name  = '{}' AND booking_agent.booking_agent_id = purchases.booking_agent_id AND purchases.ticket_id = ticket.ticket_id and purchases.purchase_date >= date_sub(now(),INTERVAL 12 MONTH) and purchases.booking_agent_id is not null\
					group by booking_agent.email\
					ORDER BY count DESC\
					limit 5;"
		cursor.execute(query_2.format(airline))
		rows2 = cursor.fetchall()
		query_3 = "select booking_agent.email, purchases.booking_agent_id, sum(flight.price * 0.1) as commission\
				from purchases,ticket, flight, booking_agent\
				where booking_agent.booking_agent_id = purchases.booking_agent_id AND flight.airline_name  = '{}' AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND \
				purchases.ticket_id = ticket.ticket_id and purchases.purchase_date >= date_sub(now(),INTERVAL 12 MONTH) and purchases.booking_agent_id is not null \
				group by booking_agent.email\
				ORDER BY commission DESC\
				limit 5"
		cursor.execute(query_3.format(airline))
		rows3 = cursor.fetchall()
		cursor.close()
		return render_template("StaffViewBookingAgent.html", rows1 = rows1, rows2 = rows2, rows3 = rows3)
	else:
		return redirect('/login')

@app.route('/StaffReports', methods = ['GET','POST'])
def StaffReports():
	if session.get('username3'):
		if request.method == 'GET':
			return render_template('StaffReports.html')
		airline = session['username3'][1]
		cursor = conn.cursor()	
		StartTime = request.form['StartTime']
		EndTime = request.form['EndTime']
		query = "select count(purchases.ticket_id),YEAR(purchase_date),MONTH(purchase_date)\
				from purchases, flight, ticket\
				where purchases.ticket_id = ticket.ticket_id AND ticket.airline_name = flight.airline_name and ticket.flight_num = flight.flight_num and flight.airline_name = '{}' and purchase_date >= '{}' and purchase_date <= '{}'\
				group by YEAR(purchase_date),MONTH(purchase_date);"
		cursor.execute(query.format(airline, StartTime, EndTime))
		result = cursor.fetchall()
		rows = {}
		startDate = datetime.strptime(StartTime,'%Y-%m-%d')
		endDate = datetime.strptime(EndTime, '%Y-%m-%d')
		year = startDate.year
		month = startDate.month
		while year <= endDate.year:
			if year == endDate.year and month == endDate.month+1:
				break
			if month <= 12:
				temp = str(year)+"-"+str(month)
				rows[temp] = 0
				month += 1
			else:
				year += 1
				month = 1
		for i in result:
			rows[str(i[1])+"-"+str(i[2])] = i[0]
		array_1 = []
		for (key,value) in rows.items():
			array_1.append([key, value])
		cursor.close()
		return jsonify(array_1)
	else:
		return redirect('/login')

@app.route('/StaffComparisonOfRevenueEarned', methods = ['GET','POST'])
def StaffComparisonOfRevenueEarned():
	# in the last month
	if session.get('username3'):
		airline = session['username3'][1]
		cursor = conn.cursor()
		query_indirect_1 = "select sum(flight.price)\
					from purchases,ticket, flight\
					where flight.airline_name  = '{}' AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND \
					purchases.ticket_id = ticket.ticket_id and purchases.purchase_date >= date_sub(now(),INTERVAL 1 MONTH) AND purchases.booking_agent_id is not null"
		cursor.execute(query_indirect_1.format(airline))
		rows3 = cursor.fetchall()
		query_direct_1 = "select sum(flight.price)\
					from purchases,ticket, flight\
					where flight.airline_name  = '{}' AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND \
					purchases.ticket_id = ticket.ticket_id and purchases.purchase_date >= date_sub(now(),INTERVAL 1 MONTH) AND purchases.booking_agent_id is null"
		cursor.execute(query_direct_1.format(airline))
		rows4 = cursor.fetchall() 
		rows3_dic = {}
		rows4_dic = {}
		rows3_dic["name"] = "Indirect sale"
		rows3_dic["y"] = rows3[0][0]
		rows4_dic["name"] = "Direct sale"
		rows4_dic["y"] = rows4[0][0]
		cursor.close()
		# in the last year
		cursor = conn.cursor()
		query_indirect = "select sum(flight.price)\
					from purchases,ticket, flight\
					where flight.airline_name  = '{}' AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND \
					purchases.ticket_id = ticket.ticket_id and purchases.purchase_date >= date_sub(now(),INTERVAL 12 MONTH) AND purchases.booking_agent_id is not null"
		cursor.execute(query_indirect.format(airline))
		rows1 = cursor.fetchall()
		query_direct = "select sum(flight.price)\
					from purchases,ticket, flight\
					where flight.airline_name  = '{}' AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num  AND \
					purchases.ticket_id = ticket.ticket_id and purchases.purchase_date >= date_sub(now(),INTERVAL 12 MONTH) AND purchases.booking_agent_id is null"
		cursor.execute(query_direct.format(airline))
		rows2 = cursor.fetchall() 
		rows1_dic = {}
		rows2_dic = {}
		rows1_dic["name"] = "Indirect sale"
		rows1_dic["y"] = rows1[0][0]
		rows2_dic["name"] = "Direct sale"
		rows2_dic["y"] = rows2[0][0]
		cursor.close()
		return render_template("staffComparisonOfRevenueEarned.html", my_array = r'[{name:"Indirect sale", y:%d}, {name:"Direct sale", y: %d}]' % (rows3[0][0], rows4[0][0]), my_array2 = r'[{name:"Indirect sale", y:%d}, {name:"Direct sale", y: %d}]' % (rows1[0][0], rows2[0][0]))
	else:
		return redirect('/login')

@app.route('/StaffViewTopDestinations', methods = ['GET','POST'])
def StaffViewTopDestinations():
	if session.get('username3'):
		airline = session['username3'][1]
		cursor = conn.cursor()
		query_1 = "select airport.airport_city, count(ticket.ticket_id) as count from purchases,ticket, flight, airport\
				where flight.airline_name  = '{}' AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.airport_name AND \
				purchases.ticket_id = ticket.ticket_id AND purchase_date >= date_sub(now(),INTERVAL 3 MONTH)\
				group by airport.airport_city\
				ORDER BY count DESC\
				limit 5;"
		cursor.execute(query_1.format(airline))
		rows1 = cursor.fetchall()

		query_2 = "select airport.airport_city, count(ticket.ticket_id) as count from purchases,ticket, flight, airport\
				where flight.airline_name  = '{}' AND ticket.airline_name = flight.airline_name AND ticket.flight_num = flight.flight_num AND flight.arrival_airport = airport.airport_name AND \
				purchases.ticket_id = ticket.ticket_id AND purchase_date >= date_sub(now(),INTERVAL 12 MONTH)\
				group by airport.airport_city\
				ORDER BY count DESC\
				limit 5;"
		cursor.execute(query_2.format(airline))
		rows2 = cursor.fetchall()
		cursor.close()
		return render_template("StaffViewTopDestinations.html", rows1 = rows1, rows2 = rows2)
	else:
		return redirect('/login')
	
app.secret_key = 'some key that you will never guess'
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)

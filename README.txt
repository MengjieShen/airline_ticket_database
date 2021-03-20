#######################################################################
This is the list of files in this project
#######################################################################

blog.py -- all flasks and sql queries
Templates:
	index.html (The home page to search the flight based on source city/airport name, destination city/airport name, date and search based on flight number, arrival/departure date)
	PublicFlightinfo.html (return the searching result of index page)
	register.html (register 3 types of users in this page)
	login.html (log in 3 types of users in this page)

	Customer{
		CustomerViewMyFlights.html (View all purchased ticket)
		CustomerSearchTickets.html (search tickets in two ways and see the searching result on this page, and purchase function)
		CustomerTrackMySpending.html (view total amount of money spent within a range of time)
}


	Booking Agent{
		BookingAgentViewMyFlights.html (flights information for which purchased on behalf of customers)
		BookingAgentSearchTickets.html (search tickets in two ways and see the searching result on this page, and purchase function)
		BookingAgentViewMyCommission.html (view total amount of commission received and total numbers of tickets sold)
		BookingAgentViewTopCustomers.html (Top 5 customers based on number of tickets bought from the booking agent in the past 6 months and top 5 customers based on amount of commission received in the last year.)
}

	Airline Staff{
		StaffAddAirplane.html (Add new plane to the airline company)
		StaffAddNewAirport.html (adds a new airport)
		StaffChangeStatusofFlights.html (changes a flight status)
		StaffComparisonOfRevenueEarned.html (Total amounts of ticket sold based on range of dates/last year/last month etc. Month wise tickets sold in a bar chart. )
StaffCreateNewFlights (creates a new flight)
		StaffReports.html (Total amounts of ticket sold based on range of dates/last year/last month etc. Month wise tickets sold in a bar chart. )
		StaffViewBookingAgent.html (Top 5 booking agents based on number of tickets sales for the past month and past year. Top 5 booking agents based on the amount of commission received for the last year.)
		StaffViewFrequentCustomers.html (see the most frequent customer within the last year/ see a list of all flights a particular Customer has taken only on that particular airline. )
		StaffViewMyFlights.html (He/she will be able to see all the current/future/past flights operated by the airline he/she works for based range of dates, and see all the customers of a particular flight. )
		StaffViewTopDestinations.html (Find the top 3 most popular destinations for last 3 months and last year. )
}

	static{
		css (animate frame / style frame)
		Fonts (fonts used in the html)
		Images (used for banner)
		Js (style frame)
}
	
###############################################################
	
Authors: Tianyu Zhang, Mengjie Shen

Project Orientation:
UI Design and data organization: Tianyu Zhang

SQL and flask: Mengjie Shen

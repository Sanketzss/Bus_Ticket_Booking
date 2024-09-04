import mysql.connector
from datetime import datetime

database = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='sanket1234',
    database='bus_ticketing'
)

connection = database.cursor()
create_table_query = '''
CREATE TABLE IF NOT EXISTS bookings (
    Passenger_Id INT AUTO_INCREMENT PRIMARY KEY,
    Passenger_Name VARCHAR(255),
    Passenger_Age INT,
    No_of_passengers INT,
    Date_of_travel DATE,
    Price FLOAT
)
'''
connection.execute(create_table_query)

TOTAL_SEATS = 40

def display_menu():
    print("1. Seat Availability")
    print("2. Booking")
    print("3. Show all bookings")
    print("4. Update Booking Details")
    print("5. Cancel Booking")
    print("6. Exit Application")


def check_seat_availability(date_of_travel):
    query = "SELECT SUM(No_of_passengers) FROM bookings WHERE Date_of_travel = %s"
    connection.execute(query, (date_of_travel,))
    booked_seats = connection.fetchone()[0]
    booked_seats = booked_seats if booked_seats is not None else 0
    available_seats = TOTAL_SEATS - booked_seats
    print(f"Total seats booked on {date_of_travel}: {booked_seats}")
    print(f"Seats available on {date_of_travel}: {available_seats}")
    return available_seats


def book_seat():
    date_of_travel = input("Enter Date of Travel (YYYY-MM-DD): ")
    available_seats = check_seat_availability(date_of_travel)

    if available_seats > 0:
        name = input("Enter Passenger Name: ")
        age = int(input("Enter Passenger Age: "))
        num_passengers = int(input("Enter Number of Passengers: "))

        if num_passengers > available_seats:
            print(f"Only {available_seats} seats are available.")
            return

        price = float(input("Enter Price: "))

        query = '''
        INSERT INTO bookings (Passenger_Name, Passenger_Age, No_of_passengers, Date_of_travel, Price)
        VALUES (%s, %s, %s, %s, %s)
        '''
        values = (name, age, num_passengers, date_of_travel, price)
        connection.execute(query, values)
        database.commit()
        print("Booking successful!")
    else:
        print("No seats available for the selected date.")


def show_all_bookings():
    query = "SELECT * FROM bookings"
    connection.execute(query)
    results = connection.fetchall()
    for row in results:
        passenger_id, passenger_name, passenger_age, no_of_passengers, date_of_travel, price = row
        date_of_travel = date_of_travel.strftime('%Y-%m-%d')
        print((passenger_id, passenger_name, passenger_age, no_of_passengers, date_of_travel, price))


def update_booking_details():
    passenger_id = int(input("Enter Passenger ID to update: "))
    name = input("Enter new Passenger Name: ")
    age = int(input("Enter new Passenger Age: "))
    num_passengers = int(input("Enter new Number of Passengers: "))
    date_of_travel = input("Enter new Date of Travel (YYYY-MM-DD): ")
    price = float(input("Enter new Price: "))

    query = '''
    UPDATE bookings
    SET Passenger_Name = %s, Passenger_Age = %s, No_of_passengers = %s, Date_of_travel = %s, Price = %s
    WHERE Passenger_Id = %s
    '''
    values = (name, age, num_passengers, date_of_travel, price, passenger_id)
    connection.execute(query, values)
    database.commit()
    print("Booking updated successfully!")


def cancel_booking():
    passenger_id = int(input("Enter Passenger ID to cancel: "))
    query = "DELETE FROM bookings WHERE Passenger_Id = %s"
    connection.execute(query, (passenger_id,))
    database.commit()
    print("Booking cancelled successfully!")

while True:
    display_menu()
    choice = int(input("Enter your choice: "))

    if choice == 1:
        date_of_travel = input("Enter Date of Travel (YYYY-MM-DD) to check availability: ")
        check_seat_availability(date_of_travel)
    elif choice == 2:
        book_seat()
    elif choice == 3:
        show_all_bookings()
    elif choice == 4:
        update_booking_details()
    elif choice == 5:
        cancel_booking()
    elif choice == 6:
        print("Exiting application.")
        break
    else:
        print("Invalid choice. Please try again.")


connection.close()
database.close()

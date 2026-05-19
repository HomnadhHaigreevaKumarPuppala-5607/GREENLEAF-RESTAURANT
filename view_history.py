import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

print("----- ORDERS HISTORY -----")
cursor.execute("SELECT * FROM orders")
orders = cursor.fetchall()

for order in orders:
    print(order)

print("\n----- BOOKINGS HISTORY -----")
cursor.execute("SELECT * FROM bookings")
bookings = cursor.fetchall()

for booking in bookings:
    print(booking)

conn.close()
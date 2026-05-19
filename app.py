from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


# ================= DATABASE CONNECTION =================

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ================= CREATE TABLES =================

def create_tables():

    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        price INTEGER
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        date TEXT,
        time TEXT
    )
    """)

    conn.commit()
    conn.close()


create_tables()


# ================= HOME PAGE =================

@app.route("/")
def home():
    return render_template("index.html")


# ================= SAVE ORDER =================

@app.route("/order", methods=["POST"])
def order():

    data = request.json

    conn = get_db()

    for item in data["cart"]:
        conn.execute(
            "INSERT INTO orders (item_name, price) VALUES (?, ?)",
            (item["name"], item["price"])
        )

    conn.commit()
    conn.close()

    return jsonify({"message": "Order saved successfully"})


# ================= SAVE BOOKING =================

@app.route("/booking", methods=["POST"])
def booking():

    data = request.json

    conn = get_db()

    conn.execute(
        "INSERT INTO bookings (name, phone, date, time) VALUES (?, ?, ?, ?)",
        (data["name"], data["phone"], data["date"], data["time"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Booking confirmed"})


# ================= HISTORY API =================

@app.route("/history")
def history():

    conn = get_db()

    orders = conn.execute("SELECT * FROM orders").fetchall()

    conn.close()

    return jsonify({
        "orders": [dict(row) for row in orders]
    })


# ================= CLEAR HISTORY =================

@app.route("/clear_history", methods=["POST"])
def clear_history():

    conn = get_db()

    conn.execute("DELETE FROM orders")

    conn.commit()
    conn.close()

    return jsonify({"message": "History cleared"})


# ================= RUN SERVER =================

if __name__ == "__main__":
    app.run(debug=True)
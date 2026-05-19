from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


# ================= DATABASE CONNECTION =================

def get_db():

    db_path = os.path.join(
        os.path.dirname(__file__),
        "database.db"
    )

    conn = sqlite3.connect(db_path)

    conn.row_factory = sqlite3.Row

    return conn


# ================= CREATE TABLES =================

def create_tables():

    conn = get_db()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS orders(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        price INTEGER NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


create_tables()


# ================= HOME PAGE =================

@app.route("/")
def home():

    try:
        return render_template("index.html")

    except Exception as e:
        return f"""
        <h1>GreenLeaf Restaurant</h1>
        <h3>Template Error</h3>
        <p>{str(e)}</p>
        <p>Make sure templates/index.html exists.</p>
        """


# ================= SAVE ORDER =================

@app.route("/order", methods=["POST"])
def order():

    try:

        data = request.get_json()

        if not data or "cart" not in data:
            return jsonify({
                "error": "Cart data missing"
            }), 400

        conn = get_db()

        for item in data["cart"]:

            conn.execute(
                "INSERT INTO orders (item_name, price) VALUES (?, ?)",
                (
                    item.get("name", "Unknown Item"),
                    item.get("price", 0)
                )
            )

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Order saved successfully"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ================= SAVE BOOKING =================

@app.route("/booking", methods=["POST"])
def booking():

    try:

        data = request.get_json()

        conn = get_db()

        conn.execute(
            """
            INSERT INTO bookings
            (name, phone, date, time)
            VALUES (?, ?, ?, ?)
            """,
            (
                data.get("name"),
                data.get("phone"),
                data.get("date"),
                data.get("time")
            )
        )

        conn.commit()
        conn.close()

        return jsonify({
            "message": "Booking confirmed"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ================= ORDER HISTORY =================

@app.route("/history")
def history():

    try:

        conn = get_db()

        orders = conn.execute(
            "SELECT * FROM orders ORDER BY id DESC"
        ).fetchall()

        bookings = conn.execute(
            "SELECT * FROM bookings ORDER BY id DESC"
        ).fetchall()

        conn.close()

        return jsonify({

            "orders": [dict(row) for row in orders],

            "bookings": [dict(row) for row in bookings]

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ================= CLEAR HISTORY =================

@app.route("/clear_history", methods=["POST"])
def clear_history():

    try:

        conn = get_db()

        conn.execute("DELETE FROM orders")

        conn.execute("DELETE FROM bookings")

        conn.commit()
        conn.close()

        return jsonify({
            "message": "History cleared successfully"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# ================= HEALTH CHECK =================

@app.route("/health")
def health():

    return jsonify({
        "status": "running",
        "message": "GreenLeaf Restaurant API is working"
    })


# ================= TEST ROUTE =================

@app.route("/test")
def test():

    return """
    <h1>GreenLeaf Restaurant</h1>
    <h2>Server Running Successfully 🍽️</h2>
    """


# ================= RUN SERVER =================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )

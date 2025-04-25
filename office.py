from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)
DATABASE = 'delivery.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def create_tables():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS deliveries (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_name TEXT,
                          address TEXT,
                          phone TEXT,
                          status TEXT)''')
        db.commit()

@app.route('/')
def delivery_dashboard():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM deliveries")
    orders = cursor.fetchall()
    return render_template('delivery.html', orders=orders)

@app.route('/update_status/<int:order_id>/<string:new_status>')
def update_status(order_id, new_status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE deliveries SET status = ? WHERE id = ?", (new_status, order_id))
    db.commit()
    return redirect(url_for('delivery_dashboard'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for,jsonify, session, flash
import sqlite3
import os
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user




app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.secret_key = "supersecretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Ensure Correct Format
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image1 = db.Column(db.String(255), nullable=True)  # Product Image Path

# 🛒 Cart Model (Add to Cart Feature)
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
with app.app_context():
    db.create_all()


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    product_image = db.Column(db.String(200), nullable=False)
    product_details = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    # Create tables if they don't exist



@app.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        if 'user' in session:
            user_id = session.get('user_id')# જો user dictionary હોય તો id મેળવો
  # Correct way to extract ID

            # Ensure it's an integer (not a tuple)
            if isinstance(user_id, tuple):
                    user_id = user_id[0]  

            product_name = request.form.get('product_name')
            product_image = request.form.get('product_image')
            product_details = request.form.get('product_details', 'No details provided')
            quantity = request.form.get('quantity', type=int, default=1)

            # Debugging: Print values
            print(f"user_id: {user_id}, Type: {type(user_id)}")
            print(f"Product: {product_name}, Image: {product_image}, Details: {product_details}, Quantity: {quantity}")

            if not isinstance(user_id, int):
                return "Error: Invalid user ID", 400  # Stop execution if user_id is not valid

            new_order = Order(
                user_id=user_id, 
                product_name=product_name, 
                product_image=product_image, 
                product_details=product_details, 
                quantity=quantity
            )

            db.session.add(new_order)
            return redirect(url_for('order'))
        else:
            return redirect(url_for('order'))

    if 'user' in session:
        user_orders = db.session.query(Order, user_id).join(user_id, Order.user_id == user_id).filter(Order.user_id == session['user_id']).all()
        return render_template("order.html", orders=user_orders)
    else:
        return redirect(url_for('order'))

# Initialize Database


# Ensure database tables are created before running the app

# Function to create user table
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    number TEXT,
                    email TEXT UNIQUE,
                    password TEXT,
                    address TEXT)''')
    conn.commit()
    conn.close()

# Database connection function
def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS contact_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')
    conn.commit()
    conn.close()

import sqlite3

def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Create Admin Table
    c.execute('''CREATE TABLE IF NOT EXISTS admin_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )''')

    # Create Contact Messages Table
    c.execute('''CREATE TABLE IF NOT EXISTS contact_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')

    # Create Cart Table
    c.execute('''CREATE TABLE IF NOT EXISTS Cart (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL
                )''')

    # Create Orders Table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    payment_method TEXT NOT NULL
                )''')

    # Create Order Items Table
    c.execute('''CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    total_price REAL NOT NULL,
                    image1 TEXT,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id)
                )''')

   

# Run the function to create tables
    # Insert Default Admin (Only if no admin exists)
    c.execute("SELECT * FROM admin_users")
    if not c.fetchall():
        c.execute("INSERT INTO admin_users (username, password) VALUES ('admin', 'admin123')")
    c.execute("SELECT * FROM Cart")
    if not c.fetchall():
        c.execute("INSERT INTO Cart(id, user_id,product_id,quantity) VALUES ('1', '1','1', '1')")

    conn.commit()
    conn.close()

# Admin Login Route
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM admin_users WHERE username=? AND password=?", (username, password))
        admin = c.fetchone()
        conn.close()

        if admin:
            session['admin'] = username  # Store in session
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error="Invalid Credentials")

    return render_template('admin_login.html')

# Admin Dashboard Route
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contact_messages")
   
    messages = c.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', messages=messages)

@app.route('/admin/users')
def manage_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, first_name, last_name, number, email FROM users")
    users = c.fetchall()
    conn.close()
    return render_template('manage_users.html', users=users)


@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("User deleted successfully!", "success")
    return redirect(url_for('manage_users'))


@app.route('/admin/edit_user/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    fname = request.form['fname']
    lname = request.form['lname']
    number = request.form['number']
    email = request.form['email']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET first_name = ?, last_name = ?, number = ?, email = ? WHERE id = ?", 
              (fname, lname, number, email, user_id))
    conn.commit()
    conn.close()
    
    flash("User updated successfully!", "success")
    return redirect(url_for('manage_users'))

@app.route('/feedback')
def feedback():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM contact_messages")
   
    messages = c.fetchall()
    conn.close()

    return render_template('feedback.html', messages=messages)

@app.route('/about')
def about():
    
    user = session.get('user') 
    return render_template('about.html',user=user)

# Admin Logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))


# Contact page route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    
    user = session.get('user') 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Insert data into database
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)", 
                  (name, email, message))
        conn.commit()
        conn.close()
        
        
        return redirect(url_for('contact'))  # Redirect after submission

    return render_template('contact.html', user=user)


# Function to create products table
def create_products_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price REAL,
                    stock INTEGER,
                    category TEXT,
                    description TEXT,
                    image1 TEXT)''')
    conn.commit()
    conn.close()
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    user = session.get('user')

    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # ✅ Yeh dictionary-style access enable karega
    c = conn.cursor()
    c.execute("SELECT * FROM products LIMIT 12")
    products = c.fetchall()
    conn.close()


    return render_template('index.html', user=user, products=products)
@app.route('/session-check')
def session_check():
    return f"User ID in session: {session.get('user_id', 'No session found')}"

@app.route('/register', methods=['POST'])
def register():
    fname = request.form['fname']
    lname = request.form['lname']
    number = request.form['number']
    email = request.form['email']
    password = request.form['setpass']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if email already exists
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    existing_user = c.fetchone()
    
    if existing_user:
        conn.close()
        flash("Email already registered! Try another email.", "error")
        return redirect(url_for('index'))

    # Insert new user
    c.execute("INSERT INTO users (first_name, last_name, number, email, password) VALUES (?, ?, ?, ?, ?)", 
              (fname, lname, number, email, password))
    conn.commit()

    # Auto-login after registration
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    session['user'] = user
    session['user_id'] = user[0]
    
    session['user_e'] = user[4]   # Storing user_id
    
    conn.close()

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['userr']
    password = request.form['pass']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()

    if user:
        session['user'] = user
        session['user_id'] = user[0] 
          # Storing user_id
        return redirect(url_for('index'))
        
    return "Invalid Credentials"

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))



def get_db_connection():
   
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_order_id():
    """Generate a unique order ID based on timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"ORD{timestamp}"

@app.route('/delivery_officer')
def delivery_officer():
    if "delivery_officer_id" not in session:
        return redirect(url_for("delivery_officer_login"))
    
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all orders with their statuses
    cursor.execute("SELECT order_id, name, address, phone, email, payment_method, status FROM orders")
    orders = cursor.fetchall()
    
    conn.close()
    return render_template("delivery_officer.html", orders=orders)

# Route to update order status
@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    try:
        order_id = request.form.get("order_id")
        new_status = request.form.get("status")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, order_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Order status updated successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/track_order")
def track_order():
    order_id = request.args.get("order_id")
    
    if not order_id:
        return "ऑर्डर ID आवश्यक है!", 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # ऑर्डर डिटेल्स प्राप्त करें
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()
    
    # Fetch order items
    cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    order_items = cursor.fetchall()

    conn.close()


    if not order:
        return "कोई ऑर्डर नहीं मिला!", 404

    conn.close()

    return render_template("order_tracking.html", order=order, order_items=order_items)
@app.route("/place_order", methods=["POST"])
def place_order():
    try:
        print("Request received")  # Debugging step
        name = request.form.get("name")
        address = request.form.get("address")
        phone = request.form.get("phone")
        email = request.form.get("email")
        payment_method = request.form.get("payment")
        order_id = generate_order_id()
        acc_email = request.form.get("acc_email")  # अब session से email ले रहे हैं

        print("Order ID:", order_id)
        print("Name:", name)
        print("Address:", address)
        print("Phone:", phone)
        print("Payment Method:", acc_email)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if orders table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        table_exists = cursor.fetchone()
        if not table_exists:
            return jsonify({"error": "Orders table does not exist"}), 500

        # 🛒 **Order Insert करना**
        cursor.execute("INSERT INTO orders (order_id, name, address, phone, email, acc_email, payment_method) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (order_id, name, address, phone, email, acc_email, payment_method))

        cart_items = request.form.getlist("cart_items[]")

        for item in cart_items:
            product_name, price, quantity, img = item.split(",")  
            total_price = float(price) * int(quantity)

            # 🔹 **Order Items में Insert करना**
            cursor.execute("INSERT INTO order_items (order_id, product_name, price, quantity, total_price, image1) VALUES (?, ?, ?, ?, ?, ?)",
                           (order_id, product_name, price, quantity, total_price, img))

        # 🛒 **Cart से आइटम Remove करना**
        cursor.execute("DELETE FROM Cart WHERE user_id = ?", (session.get("user_id"),))

        conn.commit()
        conn.close()

        return jsonify({"message": "Order placed successfully!", "order_id": order_id})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# 🔥 Route to Show Orders in Admin Panel
@app.route("/admin/orders")
def manage_orders():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        conn.close()
        
        return render_template("order_manage.html", orders=orders)
    
    except Exception as e:
        return f"Error Fetching Orders: {str(e)}"

# 🚀 Route to Delete an Order
@app.route("/delete_order/<order_id>")
def delete_order(order_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        conn.commit()
        conn.close()
        flash("Order Deleted Successfully!", "success")
        
        return redirect(url_for("manage_orders"))
    
    except Exception as e:
        return f"Error Deleting Order: {str(e)}"
    
@app.route("/order_details")
def order_details():
    order_id = request.args.get("order_id")

    if not order_id:
        return "Order ID is required!", 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch order details
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()

    # Fetch order items
    cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
    order_items = cursor.fetchall()

    conn.close()

    if not order:
        return "Order not found!", 404

    return render_template("order_details.html", order=order, order_items=order_items)


@app.route("/delivery_officer_login", methods=["GET", "POST"])
def delivery_officer_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM delivery_officers WHERE email = ? AND password = ?", (username, password))
        officer = cursor.fetchone()
        conn.close()

        if officer:
            session["delivery_officer_id"] = officer["id"]
            session["delivery_officer_username"] = officer["email"]
            return redirect(url_for("delivery_officer_dashboard"))
        else:
            return render_template("delivery_officer_login.html", error="Invalid username or password!")

    return render_template("delivery_officer_login.html")

# Delivery Officer Dashboard Route
@app.route("/delivery_officer_dashboard")
def delivery_officer_dashboard():
    if "delivery_officer_id" not in session:
        return redirect(url_for("delivery_officer_login"))
       
    return redirect(url_for('delivery_officer'))
# Logout Route
@app.route("/logout1")
def logout1():
    session.pop('delivery_officer_id', None)
    session.pop('delivery_officer_username', None)
    
    return redirect(url_for("delivery_officer_login"))


@app.route("/manage_officers")
def manage_officers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM delivery_officers")
    officers = cursor.fetchall()
    conn.close()
    return render_template("manage_delivery_officers.html", officers=officers)

@app.route("/add_officer", methods=["POST"])
def add_officer():
    name = request.form.get("name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    password = request.form.get("password")  # Hash password before storing

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO delivery_officers (name, phone, email, password) VALUES (?, ?, ?, ?)",
                   (name, phone, email, password))
    conn.commit()
    conn.close()

    return redirect(url_for("manage_officers"))

@app.route("/delete_officer/<int:officer_id>")
def delete_officer(officer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM delivery_officers WHERE id = ?", (officer_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("manage_officers"))

@app.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    brands = ["Rolex",  "Patek Philippe", "Titan", "Hublot", "Diamond Watch"]  # Example brands

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Fetch product details
    c.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = c.fetchone()
    
    if not product:
        conn.close()
        flash("Product not found!", "error")
        return redirect(url_for('products'))

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']
        category = request.form['category']
        description = request.form['description']

        images = list(product[6:10])  # Fetch existing images (columns 6-9)

        for i in range(4):
            file = request.files.get(f'image{i+1}')
            if file and file.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                images[i] = file.filename  # Update only if a new file is uploaded

        c.execute("""
            UPDATE products 
            SET name=?, price=?, stock=?, category=?, description=?, image1=?, image2=?, image3=?, image4=? 
            WHERE id=?
        """, (name, price, stock, category, description, *images, product_id))

        conn.commit()
        conn.close()
        
        flash("✅ Product updated successfully!", "success")
        return redirect(url_for('products'))

    conn.close()
    return render_template('edit_product.html',brands=brands, product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    
    # Pehle check karein ki product exist karta hai ya nahi
    c.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = c.fetchone()
    
    if not product:
        conn.close()
        flash("❌ Product not found!", "error")
        return redirect(url_for('show_products'))

    # Product delete karna
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()
    
    flash("✅ Product deleted successfully!", "success")
    return redirect(url_for('products'))  # Corrected redirect

@app.route('/product/<int:product_id>')
def product_details(product_id):
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # પ્રોડક્ટ શોધો
    c.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = c.fetchone()
    conn.close()

    if not product:
       
        return redirect(url_for('index'))  # Redirect if product not found

    return render_template('product_details.html', product=product)
@app.route('/brand/<category>')
def brand(category):
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # પ્રોડક્ટ શોધો જે આ કેટેગરી સાથે મેળ ખાય
    c.execute("SELECT id,name, price, stock, description, image1 FROM products WHERE category=?", (category,))
    watches = c.fetchall()
    
    conn.close()

    if not watches:
       
        return redirect(url_for('collection'))  

    return render_template('brand.html', brand=category, watches=watches)
@app.route('/check_login')
def check_login():
    if 'user_id' in session:
        return jsonify({"status": "logged_in", "user_id": session['user_id']})
    else:
        return jsonify({"status": "not_logged_in"}), 401


# 🟢 Add to Cart@app.route('/add_to_cart/<int:product_id>')
@app.route('/add_to_cart/<int:product_id>', methods=['GET', 'POST'])
def add_to_cart(product_id):
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user_id = session['user_id']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if product already exists in the cart
    c.execute("SELECT quantity FROM Cart WHERE user_id = ? AND product_id = ?", (user_id, product_id))
    existing_product = c.fetchone()

    if existing_product:
        # If product exists, update quantity
        new_quantity = existing_product[0] + 1
        c.execute("UPDATE Cart SET quantity = ? WHERE user_id = ? AND product_id = ?", (new_quantity, user_id, product_id))
    else:
        # If product does not exist, insert new record
        c.execute("INSERT INTO Cart(user_id, product_id, quantity) VALUES (?, ?, ?)", (user_id, product_id, 1))

    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))  # Corrected redirect

@app.route('/check_cart')
def check_cart():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Cart")
    data = c.fetchall()
    conn.close()
@app.route('/cart')
def view_cart():
    if 'user_id' not in session:
        return redirect(url_for('index'))  # User not logged in, redirect to login

    user_id = session['user_id']
    user = session.get('user')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()       

    # Fetch cart items along with product image
    c.execute('''
        SELECT Cart.id, Products.name, Products.price, Cart.quantity, Products.image1
        FROM Cart 
        INNER JOIN Products ON Cart.product_id = Products.id 
        WHERE Cart.user_id = ?
    ''', (user_id,))
    
    cart_items = c.fetchall()
    conn.close()

    return render_template('cart.html', cart_items=cart_items  ,user=user)
@app.route("/my_orders")
def my_orders():
    if "user_id" not in session:  # Check if user is logged in
        return redirect(url_for("login"))

    user_name = session["user_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # 🔹 Username के आधार पर User की Email निकालो
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_name,))
    user_email = cursor.fetchone()

    if not user_email:
        return "User email not found!", 404

    acc_email = user_email[0]

    # 🔹 Orders निकालो जहाँ acc_email Logged-in User की Email के बराबर हो
    cursor.execute("SELECT order_id, name, address, phone, payment_method, status FROM orders WHERE acc_email = ?", (acc_email,))
    orders = cursor.fetchall()

    conn.close()

    return render_template("my_orders.html", orders=orders)


@app.route('/remove_one/<int:cart_id>', methods=['POST'])
def remove_one(cart_id):
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user_id = session['user_id']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if the product exists in cart
    c.execute("SELECT quantity FROM Cart WHERE id = ? AND user_id = ?", (cart_id, user_id))
    existing_product = c.fetchone()

    if existing_product:
        if existing_product[0] > 1:
            c.execute("UPDATE Cart SET quantity = quantity - 1 WHERE id = ? AND user_id = ?", (cart_id, user_id))
        else:
            c.execute("DELETE FROM Cart WHERE id = ? AND user_id = ?", (cart_id, user_id))

        conn.commit()
        conn.close()
        return jsonify({'message': 'One quantity removed'})
    else:
        conn.close()
        return jsonify({'message': 'Product not found'}), 404

@app.route('/remove_all/<int:cart_id>', methods=['POST'])
def remove_all(cart_id):
    if 'user_id' not in session:
        return jsonify({'message': 'User not logged in'}), 401

    user_id = session['user_id']
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("DELETE FROM Cart WHERE id = ? AND user_id = ?", (cart_id, user_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'All quantities removed'})

@app.route('/products')
def products():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")  # Database se sare products fetch kar rahe hain
    products = c.fetchall()
    conn.close()
    return render_template('products.html', products=products)

import sqlite3

def dict_factory(cursor, row):
    """ Convert database row objects to dictionary """
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/product1')
def product1():
    conn = sqlite3.connect('users.db')
    conn.row_factory = dict_factory  # Convert tuples to dictionaries
    c = conn.cursor()
    c.execute("SELECT * FROM products")  
    products = c.fetchall()  # List of dictionaries instead of tuples
    conn.close()

    user = session.get('user')  # User session se fetch kar rahe hain
    return render_template('product1.html', products=products, user=user)


@app.route('/collection')
def collection():
    brands = ["Rolex",  "Patek Philippe", "Titan", "Hublot", "Diamond Watch"]  

    watches = {
        "Titan": [
            {"name": "Titan Classic", "image": "TI1.webp"},
            {"name": "Titan Edge", "image": "TI2.webp"},
            {"name": "Titan Octane", "image": "TI3.webp"}
        ],
        "Hublot": [
            {"name": "Hublot Big Bang", "image": "HU1.webp"},
            {"name": "Hublot Classic Fusion", "image": "HU2.webp"},
            {"name": "Hublot Spirit of Big Bang", "image": "HU3.webp"}
        ],
        "Rolex": [
            {"name": "Rolex Submariner", "image": "RX1.webp"},
            {"name": "Rolex Daytona", "image": "RX2.webp"},
            {"name": "Rolex Explorer", "image": "RX3.webp"}
        ],
        "Patek Philippe": [
            {"name": "Patek Nautilus", "image": "PP4.webp"},
            {"name": "Patek Aquanaut", "image": "PP2.webp"},
            {"name": "Patek Calatrava", "image": "PP3.webp"}
        ],
        "Diamond Watch": [
            {"name": "Luxury Diamond Watch", "image": "DM2.webp"},
            {"name": "Gold Diamond Watch", "image": "DM3.webp"},
            {"name": "Platinum Diamond Watch", "image": "DM4.webp"}
        ]
    }
    user = session.get('user') 
    return render_template("collection.html", brands=brands, watches=watches , user=user)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    brands = ["Rolex",  "Patek Philippe", "Titan", "Hublot", "Diamond Watch","other"]  # Example brands

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        stock = request.form['stock']
        category = request.form['category']
        description = request.form['description']

        images = []
        for i in range(1, 5):
            file = request.files.get(f'image{i}')
            if file and file.filename != '':
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                images.append(file.filename)
            else:
                images.append(None)

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, price, stock, category, description, image1, image2, image3, image4) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (name, price, stock, category, description, *images))
        conn.commit()
        conn.close()

        flash("✅ Product added successfully!", "success")
        return redirect(url_for('add_product'))

    return render_template('add_product.html', brands=brands)

if __name__ == '__main__':
    create_db()  # Ensure user table exists
    create_products_table()
    create_database() 
    app.run(port=5001)  # Ensure product table exists
    app.run(debug=True)
    

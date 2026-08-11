from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from delivery import stores
import random
import sqlite3
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "temporary-secret-key")


connection = sqlite3.connect("users.db")

cursor = connection.cursor()

cursor.execute(""" CREATE TABLE IF NOT EXISTS users 
      ( id INTEGER PRIMARY KEY AUTOINCREMENT, 
       name TEXT NOT NULL,
       email TEXT UNIQUE NOT NULL,
       phone TEXT NOT NULL,
       address TEXT,
      password TEXT NOT NULL ) """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_id TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    total INTEGER NOT NULL,
    payment TEXT NOT NULL,
    order_date TEXT NOT NULL
)
""")

connection.commit()
connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/stores")
def show_stores():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "").lower()

    filtered_stores = []

    if search == "":
        filtered_stores = stores

    else:
        for store in stores:

            if search in store.name.lower():
                filtered_stores.append(store)

    return render_template(
        "stores.html",
        stores=filtered_stores,
        search=search
    )


@app.route("/menu/<int:store_id>")
def menu(store_id):

    if "user_id" not in session:
        return redirect("/login")

    if "store_id" in session:

        if str(store_id) != str(session["store_id"]):
            return render_template("restaurant_warning.html")

    selected_store = None

    for store in stores:

        if store.store_id == store_id:
            selected_store = store
            break

    if selected_store:

        return render_template(
            "menu.html",
            store=selected_store,
            store_id=store_id
        )

    return "Store not found"

        
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():

    if "user_id" not in session:
        return redirect("/login")

    food = request.form["food"]
    price = int(request.form["price"])
    quantity = int(request.form["quantity"])
    store_id = request.form["store_id"]

    # -----------------------------
    # CHECK STORE
    # -----------------------------

    if "store_id" not in session:

        session["store_id"] = store_id

    else:

        if session["store_id"] != store_id:

            return render_template("restaurant_warning.html")


    # -----------------------------
    # GET CART
    # -----------------------------

    cart = session.get("cart", [])

    item_exists = False


    # -----------------------------
    # CHECK EXISTING ITEM
    # -----------------------------

    for item in cart:

        if (
            item["food"] == food
            and item["store_id"] == store_id
        ):

            item["quantity"] += quantity

            item_exists = True

            break


    # -----------------------------
    # ADD NEW ITEM
    # -----------------------------

    if not item_exists:

        cart.append({

            "food": food,

            "price": price,

            "quantity": quantity,

            "store_id": store_id

        })


    # -----------------------------
    # SAVE CART
    # -----------------------------

    session["cart"] = cart

    session["cart_count"] = sum(
        item["quantity"]
        for item in cart
    )

    session.modified = True


    return redirect(
        url_for("menu", store_id=store_id)
    )
@app.route("/cart")
def cart():
    if "user_id" not in session:
        return redirect("/login")

    items = session.get("cart", [])

    if not items:
        return render_template(
            "cart.html",
            items=[],
            grand_total=0,
            delivery_fee=0,
            items_total=0
        )


    # -----------------------------
    # ITEMS TOTAL
    # -----------------------------

    items_total = 0

    for item in items:

        items_total += (
            item["price"] *
            item["quantity"]
        )


    # -----------------------------
    # FIND STORE
    # -----------------------------

    store_id = session.get("store_id")

    selected_store = None

    for store in stores:

        if str(store.store_id) == str(store_id):

            selected_store = store

            break


    # -----------------------------
    # DELIVERY FEE
    # -----------------------------

    delivery_fee = 0

    if selected_store:

        delivery_fee = selected_store.delivery_fee


    # -----------------------------
    # FINAL TOTAL
    # -----------------------------

    grand_total = items_total + delivery_fee


    return render_template(

        "cart.html",

        items=items,

        items_total=items_total,

        delivery_fee=delivery_fee,

        grand_total=grand_total,

        store=selected_store
    )

@app.route("/clear_cart")
def clear_cart():

    session.pop("cart", None)
    session.pop("cart_count", None)
    session.pop("store_id", None)

    return redirect("/stores")

@app.route("/checkout")
def checkout():
    if "user_id" not in session:
        return redirect("/login")

    items = session.get("cart", [])

    if not items:
        return redirect("/stores")


    # -----------------------------
    # ITEMS TOTAL
    # -----------------------------

    items_total = 0

    for item in items:

        items_total += (
            item["price"] *
            item["quantity"]
        )


    # -----------------------------
    # FIND STORE
    # -----------------------------

    store_id = session.get("store_id")

    selected_store = None

    for store in stores:

        if str(store.store_id) == str(store_id):

            selected_store = store

            break


    delivery_fee = 0

    if selected_store:

        delivery_fee = selected_store.delivery_fee


    grand_total = items_total + delivery_fee


    return render_template(

        "checkout.html",

        items=items,

        items_total=items_total,

        delivery_fee=delivery_fee,

        grand_total=grand_total
        
    )
@app.route("/place_order", methods=["POST"])
def place_order():

    if "user_id" not in session:
        return redirect("/login")

    name = request.form["name"]
    phone = request.form["phone"]
    address = request.form["address"]

    items = session.get("cart", [])

    if not items:
        return redirect("/stores")


    grand_total = 0

    for item in items:
        grand_total += item["price"] * item["quantity"]


    session["order"] = {

        "name": name,
        "phone": phone,
        "address": address,
        "items": items,
        "total": grand_total

    }


    return redirect("/payment")
@app.route("/payment")
def payment():

    if "user_id" not in session:
        return redirect("/login")

    if "order" not in session:
        return redirect("/stores")


    order = session["order"]


    return render_template(
        "payment.html",
        order=order
    )


@app.route("/confirm_order", methods=["POST"])
def confirm_order():

    if "user_id" not in session:
        return redirect("/login")

    payment_method = request.form["payment"]

    if "order" not in session:
        return redirect("/stores")

    order = session["order"]

    order["payment"] = payment_method

    order_id = "HUN" + str(random.randint(10000, 99999))

    order["order_id"] = order_id

    order_date = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    # Connect to database
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Save order in database
    cursor.execute("""
        INSERT INTO orders
        (user_id, order_id, name, phone, address, total, payment, order_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session["user_id"],
        order_id,
        order["name"],
        order["phone"],
        order["address"],
        order["total"],
        payment_method,
        order_date
    ))
    

    connection.commit()
    connection.close()

    # Keep current order for order_success page
    session["order"] = order

    # Clear cart
    session.pop("cart", None)
    session.pop("cart_count", None)
    session.pop("store_id", None)

    return redirect("/order_success")


@app.route("/order_success")
def order_success():
    if "user_id" not in session:
        return redirect("/login")

    if "order" not in session:
        return redirect("/stores")


    print(session["order"])


    return render_template(
        "order_success.html",
        order=session["order"]
    )


@app.route("/orders")
def orders():

    # User must be logged in
    if "user_id" not in session:
        return redirect("/login")

    # Connect to database
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()

    # Get only this user's orders
    cursor.execute("""
        SELECT order_id,
               name,
               phone,
               address,
               total,
               payment,
               order_date
        FROM orders
        WHERE user_id = ?
        ORDER BY id DESC
    """, (session["user_id"],))

    orders = cursor.fetchall()

    connection.close()

    return render_template(
        "orders.html",
        orders=orders
    )



@app.route("/search_food")
def search_food():

    if "user_id" not in session:
        return redirect("/login")

    search = request.args.get("search", "").lower()

    results = []

    if search:

        for store in stores:

            for category, foods in store.menu.items():

                for food, price in foods.items():

                    if search in food.lower():

                        results.append({

                            "store": store,
                            "food": food,
                            "price":price,
                            "category": category

                        })

    return render_template(
        "search_food.html",
        results=results,
        search=search
    )



@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        try:

            cursor.execute("""
                INSERT INTO users
                (name, email, phone, address, password)
                VALUES (?, ?, ?, ?, ?)
            """, (
                name,
                email,
                phone,
                address,
                hashed_password
            ))

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()

            return render_template(
                "signup.html",
                error="Email already registered."
            )

        connection.close()

        return render_template(
            "signup.html",
            success="Account created successfully! 🎉"
        )

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        connection = sqlite3.connect("users.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, email, phone,address, password
            FROM users
            WHERE email = ?
        """, (email,))

        user = cursor.fetchone()

        connection.close()

        if user and check_password_hash(user[5], password):

            session["user_id"] = user[0]

            session["user"] = {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "phone": user[3],
                "address": user[4]
            }

            return redirect("/account")

        return "Invalid email or password."

    return render_template("login.html")

@app.route("/account")
def account():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("account.html")

@app.route("/logout")
def logout():

    session.pop("user_id", None)
    session.pop("user", None)

    return redirect("/login")
if __name__ == "__main__":
    app.run(debug=True) 
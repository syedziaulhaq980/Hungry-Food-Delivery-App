from flask import Flask, render_template,request, session,redirect
from delivery import stores
import random


app = Flask(__name__)
app.secret_key = "hungry_secret_key"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/stores")
def show_stores():

    search = request.args.get("search", "").lower()
    print("Search =", search)

    filtered_stores = []

    if search == "":
        filtered_stores = stores

    else:

        for store in stores:

            print(store.name)

            if search in store.name.lower():

                filtered_stores.append(store)
    
    return render_template(
        "stores.html",
        stores=filtered_stores,
        search=search
    )



@app.route("/menu/<int:store_id>")
def menu(store_id):
    if "store_id" in session:

        if str(store_id) != session["store_id"]:

            return render_template("restaurant_warning.html")

    selected_store = None


    for store in stores:
        if store.store_id == store_id:
            selected_store = store
            break
    print(selected_store)  

    if selected_store:
        return render_template(
            "menu.html",
            store = selected_store,
            store_id = store_id
        )    
    return "store Not found"

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():

    food = request.form["food"]
    price = int(request.form["price"])
    quantity = int(request.form["quantity"])
    store_id = request.form["store_id"]

    if "store_id" not in session:
        session["store_id"] = store_id

    cart = session.get("cart", [])

    item_exists = False

    for item in cart:
        if item["food"] == food and item.get("store_id") == store_id:
            item["quantity"] += quantity
            item_exists = True
            break

    if not item_exists:
        item = {
            "food": food,
            "price": price,
            "quantity": quantity,
            "store_id" : store_id
        }

        cart.append(item)

    session["cart"] = cart

    session["cart_count"] = sum(
         item["quantity"] for item in cart
        )

    return redirect(f"/menu/{store_id}")

@app.route("/cart")
def cart():

    items = session.get("cart", [])

    grand_total = 0

    for item in items:
        grand_total += item["price"] * item["quantity"]

    return render_template(
        "cart.html",
        items=items,
        grand_total=grand_total
    )

@app.route("/clear_cart")
def clear_cart():

    session.pop("cart", None)
    session.pop("cart_count", None)
    session.pop("store_id", None)

    return redirect("/stores")

@app.route("/checkout")
def checkout():

    items = session.get("cart", [])

    if not items:
        return redirect("/stores")

    grand_total = 0

    for item in items:
        grand_total += item["price"] * item["quantity"]


    return render_template(
        "checkout.html",
        items=items,
        grand_total=grand_total
    )
@app.route("/place_order", methods=["POST"])
def place_order():

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

    if "order" not in session:
        return redirect("/stores")


    order = session["order"]


    return render_template(
        "payment.html",
        order=order
    )

@app.route("/confirm_order", methods=["POST"])
def confirm_order():

    payment_method = request.form["payment"]

    if "order" not in session:
        return redirect("/stores")


    order = session["order"]

    order["payment"] = payment_method



    order_id = "HUN" + str(random.randint(10000,99999))

    order["order_id"] = order_id

    session["order"] = order

    orders = session.get("orders", [])

    orders.append(order)

    session["orders"] = orders
    
    session.pop("cart", None)

    session.pop("cart_count", None)

    session.pop("store_id", None)


    return redirect("/order_success")

@app.route("/order_success")
def order_success():

    if "order" not in session:
        return redirect("/stores")


    print(session["order"])


    return render_template(
        "order_success.html",
        order=session["order"]
    )

@app.route("/orders")
def orders():

    orders = session.get("orders", [])

    return render_template(
        "orders.html",
        orders=orders
    )

@app.route("/search_food")
def search_food():

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

if __name__ == "__main__":
    app.run(debug=True) 
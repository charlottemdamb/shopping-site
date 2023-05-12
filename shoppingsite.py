"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session
import jinja2
import melons
import os

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = os.environ['SECRET_KEY']

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""
    
    # - check if a "cart" exists in the session, and create one (an empty
    #   dictionary keyed to the string "cart") if not
    print(session)

    """""""""
    User's request includes an encrypted string (the cookie)
    Flask DESERIALIZES that, unencrypts it, and makes the session dict

    session = {
        'cart': {
            'cren': 2,
            'ali': 5,
        }
    } 

    When we send our response, Flask SERILIAZES this dictionary
    That string representation is then encrypted
    """
    
    if 'cart' not in session: #see if cart is created
        basket = session['cart'] = {}
    else:
        basket = session['cart']

    # - check if the desired melon id is the cart, and if not, put it in
    basket[melon_id]= basket.get(melon_id, 0) +1
    session.modified = True


    
    # - flash a success message
    flash("Item added to cart!")

    # - redirect the user to the cart page
    return redirect("/cart")


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # TODO: Display the contents of the shopping cart.

    # The logic here will be something like:
    #
    # - get the cart dictionary from the session
    cart = []
    cart_total = 0
    melon_total = 0

    """
    
    """

    basket = session.get('cart', {})
    
    for melon_id, qty in basket.items():
        melon = melons.get_by_id(melon_id)
        cart.append(melon)
        melon_total = qty * melon.price
        cart_total = cart_total + melon_total
        melon.quantity = qty
        melon.total_price = melon_total
    

    return render_template("cart.html", total_price = cart_total, cart = cart)


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    # The logic here should be something like:
    #
    # - get user-provided name and password from request.form
    # - use customers.get_by_email() to retrieve corresponding Customer
    #   object (if any)
    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    # - if they match, store the user's email in the session, flash a success
    #   message and redirect the user to the "/melons" route
    # - if they don't, flash a failure message and redirect back to "/login"
    # - do the same if a Customer with that email doesn't exist

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")

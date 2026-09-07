from flask import Blueprint, render_template, redirect, url_for, session, flash
from flask_login import login_required
from extensions import db
from models import Product

cart_bp = Blueprint("cart", __name__)


def get_cart():
    return session.setdefault("cart", {})


@cart_bp.route("/cart")
@login_required
def cart():
    cart_data = get_cart()
    items = []
    total = 0.0

    for product_id, item in cart_data.items():
        product = db.session.get(Product, int(product_id))
        if not product:
            continue
        quantity = int(item["quantity"])
        # Dataset prices include packaging text, so display the price exactly as supplied.
        items.append({"product": product, "quantity": quantity})
    return render_template("cart.html", items=items, total=total)


@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for("products.products"))

    cart = get_cart()
    key = str(product_id)
    if key in cart:
        cart[key]["quantity"] += 1
    else:
        cart[key] = {"quantity": 1, "name": product.medicine}

    session.modified = True
    flash(f"{product.medicine} added to cart.", "success")
    return redirect(request_referrer_or_product(product_id))


def request_referrer_or_product(product_id):
    from flask import request
    return request.referrer or url_for("products.product_detail", product_id=product_id)


@cart_bp.route("/cart/update/<int:product_id>", methods=["POST"])
@login_required
def update_cart(product_id):
    cart = get_cart()
    key = str(product_id)
    quantity = int(__import__("flask").request.form.get("quantity", 1))

    if key in cart:
        if quantity <= 0:
            cart.pop(key, None)
        else:
            cart[key]["quantity"] = min(quantity, 99)
    session.modified = True
    return redirect(url_for("cart.cart"))


@cart_bp.route("/cart/remove/<int:product_id>", methods=["POST"])
@login_required
def remove_from_cart(product_id):
    cart = get_cart()
    cart.pop(str(product_id), None)
    session.modified = True
    return redirect(url_for("cart.cart"))

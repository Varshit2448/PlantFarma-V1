import re
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from flask_login import login_required, current_user
from extensions import db
from models import Product, Order, OrderItem, OrderStatus

orders_bp = Blueprint("orders", __name__)


def numeric_price(price_text):
    if not price_text:
        return 0.0
    match = re.search(r"(\d+(?:\.\d+)?)", price_text.replace(",", ""))
    return float(match.group(1)) if match else 0.0


@orders_bp.route("/checkout")
@login_required
def checkout():
    cart = session.get("cart", {})
    items = []
    total = 0.0

    for product_id, data in cart.items():
        product = db.session.get(Product, int(product_id))
        if product:
            quantity = int(data["quantity"])
            unit = numeric_price(product.price)
            total += unit * quantity
            items.append({
                "product": product,
                "quantity": quantity,
                "unit_price": unit,
            })

    if not items:
        flash("Your cart is empty.", "error")
        return redirect(url_for("products.products"))

    return render_template("checkout.html", items=items, total=total)


@orders_bp.route("/purchase", methods=["POST"])
@login_required
def purchase():
    cart = session.get("cart", {})
    if not cart:
        flash("Your cart is empty.", "error")
        return redirect(url_for("products.products"))

    order = Order(
        farmer_id=current_user.id,
        status=OrderStatus.CONFIRMED,
        total_amount=0
    )
    db.session.add(order)
    db.session.flush()

    total = 0.0

    for product_id, data in cart.items():
        product = db.session.get(Product, int(product_id))
        if not product:
            continue

        quantity = int(data["quantity"])
        unit_price = numeric_price(product.price)
        total += unit_price * quantity

        db.session.add(OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_name=product.medicine,
            price_text=product.price,
            quantity=quantity
        ))

    order.total_amount = total
    db.session.commit()
    session["cart"] = {}
    flash("Order confirmed successfully.", "success")
    return redirect(url_for("orders.tracking", order_id=order.id))


@orders_bp.route("/orders")
@login_required
def orders():
    order_list = Order.query.filter_by(
        farmer_id=current_user.id
    ).order_by(Order.ordered_at.desc()).all()
    return render_template("orders.html", orders=order_list)


@orders_bp.route("/tracking/<int:order_id>")
@login_required
def tracking(order_id):
    order = Order.query.filter_by(
        id=order_id, farmer_id=current_user.id
    ).first_or_404()
    return render_template("tracking.html", order=order)


@orders_bp.route("/tracking/<int:order_id>/advance", methods=["POST"])
@login_required
def advance_tracking(order_id):
    # Demo tracking control. In production, status should be changed by an admin/logistics system.
    order = Order.query.filter_by(
        id=order_id, farmer_id=current_user.id
    ).first_or_404()

    statuses = [
        OrderStatus.CONFIRMED,
        OrderStatus.PROCESSING,
        OrderStatus.SHIPPED,
        OrderStatus.OUT_FOR_DELIVERY,
        OrderStatus.DELIVERED,
    ]
    try:
        index = statuses.index(order.status)
    except ValueError:
        index = 0

    if index < len(statuses) - 1:
        order.status = statuses[index + 1]
        db.session.commit()
    return redirect(url_for("orders.tracking", order_id=order.id))

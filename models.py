from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class Farmer(UserMixin, db.Model):
    __tablename__ = "farmers"

    id = db.Column(db.Integer, primary_key=True)
    kisan_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship("Order", back_populates="farmer", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    efficientnet_class = db.Column(db.String(150), index=True, nullable=False)
    crop = db.Column(db.String(100), nullable=False)
    disease = db.Column(db.String(180), nullable=False)
    medicine = db.Column(db.String(150), index=True, nullable=False)
    active_ingredient = db.Column(db.String(180), nullable=False)
    treatment_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order_items = db.relationship("OrderItem", back_populates="product", lazy=True)


class OrderStatus:
    CONFIRMED = "Confirmed"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    OUT_FOR_DELIVERY = "Out for delivery"
    DELIVERED = "Delivered"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey("farmers.id"), nullable=False)
    status = db.Column(db.String(50), default=OrderStatus.CONFIRMED, nullable=False)
    total_amount = db.Column(db.Float, nullable=False, default=0)
    ordered_at = db.Column(db.DateTime, default=datetime.utcnow)

    farmer = db.relationship("Farmer", back_populates="orders")
    items = db.relationship(
        "OrderItem", back_populates="order",
        cascade="all, delete-orphan", lazy=True
    )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    price_text = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    order = db.relationship("Order", back_populates="items")
    product = db.relationship("Product", back_populates="order_items")

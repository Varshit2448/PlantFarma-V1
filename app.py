import os

from flask import Flask, redirect, url_for, session
from flask_login import current_user

from config import Config
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    
    from routes.auth import auth_bp
    from routes.products import products_bp
    from routes.cart import cart_bp
    from routes.orders import orders_bp
    from routes.disease import disease_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(disease_bp)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("products.home"))

        return redirect(url_for("auth.login"))

    @app.context_processor
    def inject_cart_count():
        cart = session.get("cart", {})
        cart_count = sum(
            item.get("quantity", 0)
            for item in cart.values()
        )

        return {"cart_count": cart_count}

    with app.app_context():
        from models import Farmer, Product, Order, OrderItem
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
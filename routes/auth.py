from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from extensions import db, login_manager
from models import Farmer

auth_bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Farmer, int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        kisan_id = request.form.get("kisan_id", "").strip()
        password = request.form.get("password", "")

        farmer = Farmer.query.filter_by(kisan_id=kisan_id).first()
        if farmer and farmer.check_password(password):
            login_user(farmer)
            return redirect(url_for("products.home"))

        flash("Invalid Farmer/Kisan ID or password.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

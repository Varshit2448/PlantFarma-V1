from flask import Blueprint, render_template, request, abort
from flask_login import login_required
from sqlalchemy import or_, and_

from extensions import db
from models import Product


products_bp = Blueprint("products", __name__)


# ============================================================
# ONLY SHOW PRODUCTS FOR ACTUAL DISEASES
# ============================================================

def actual_disease_filter():
    """
    Keep only products that correspond to an actual disease.

    Hide:
        - Healthy
        - No curative pesticide
        - None
        - Empty disease values

    The records remain in the database.
    They are simply not displayed in the shop/home listings.
    """

    return and_(
        Product.disease.isnot(None),
        Product.disease != "",
        ~Product.disease.ilike("%healthy%"),
        ~Product.disease.ilike("%no curative pesticide%"),
        Product.medicine.isnot(None),
        Product.medicine != "",
        ~Product.medicine.ilike("none"),
    )


# ============================================================
# HOME PAGE
# ============================================================

@products_bp.route("/home")
@login_required
def home():

    featured = (
        Product.query
        .filter(
            Product.disease.isnot(None),
            Product.disease != "",
            ~Product.disease.ilike("%healthy%"),
            ~Product.treatment_type.ilike("%Management%"),
            Product.medicine.isnot(None),
            Product.medicine != "",
            ~Product.medicine.ilike("none")
        )
        .order_by(Product.id)
        .limit(8)
        .all()
    )

    return render_template(
        "home.html",
        products=featured
    )


# ============================================================
# PRODUCTS / SHOP
# ============================================================

@products_bp.route("/products")
@login_required
def products():

    q = request.args.get("q", "").strip()

    # Start with ONLY actual disease products
    query = Product.query.filter(
        actual_disease_filter()
    )

    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    if q:

        like = f"%{q}%"

        query = query.filter(
            or_(
                Product.medicine.ilike(like),
                Product.crop.ilike(like),
                Product.disease.ilike(like),
                Product.active_ingredient.ilike(like),
                Product.treatment_type.ilike(like),
                Product.efficientnet_class.ilike(like)
            )
        )

    # --------------------------------------------------------
    # DISPLAY PRODUCTS
    # --------------------------------------------------------

    products = (
        query
        .order_by(
            Product.medicine,
            Product.crop
        )
        .all()
    )

    return render_template(
        "products.html",
        products=products,
        q=q
    )


# ============================================================
# PRODUCT DETAILS
# ============================================================

@products_bp.route("/product/<int:product_id>")
@login_required
def product_detail(product_id):

    product = db.session.get(
        Product,
        product_id
    )

    if not product:
        abort(404)

    return render_template(
        "product_details.html",
        product=product
    )
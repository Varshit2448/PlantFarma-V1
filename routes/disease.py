import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename
from extensions import db
from config import Config
from models import Product
from model.disease_detection import DiseaseDetector

disease_bp = Blueprint("disease", __name__)

_detector = None


def get_detector():
    global _detector
    if _detector is None:
        _detector = DiseaseDetector(
            model_path=Config.MODEL_PATH,
            labels_path=Config.LABELS_PATH
        )
    return _detector


@disease_bp.route("/doc-kenny", methods=["GET", "POST"])
@login_required
def doc_kenny():
    if request.method == "POST":
        image = request.files.get("leaf_image")

        if not image or not image.filename:
            flash("Please select a leaf image.", "error")
            return redirect(url_for("disease.doc_kenny"))

        ext = image.filename.rsplit(".", 1)[-1].lower() if "." in image.filename else ""
        if ext not in Config.ALLOWED_EXTENSIONS:
            flash("Only PNG, JPG, JPEG and WEBP images are allowed.", "error")
            return redirect(url_for("disease.doc_kenny"))

        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(image.filename)
        path = os.path.join(Config.UPLOAD_FOLDER, filename)
        image.save(path)

        try:
            result = get_detector().predict(path)
        except Exception as exc:
            flash(f"Disease detection failed: {exc}", "error")
            return redirect(url_for("disease.doc_kenny"))

        # IMPORTANT: JSON is never rendered to the user.
        # The medicine/class is used internally to find a product row.
        product = None
        if result.get("efficientnet_class"):
            product = Product.query.filter_by(
                efficientnet_class=result["efficientnet_class"]
            ).first()

        if not product and result.get("medicine"):
            product = Product.query.filter(
                Product.medicine.ilike(result["medicine"])
            ).first()

        return render_template(
            "disease_detection.html",
            result=result,
            product=product,
            image_url=url_for("static", filename=f"uploads/{filename}")
        )

    return render_template("disease_detection.html", result=None, product=None)

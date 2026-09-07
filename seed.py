"""
One-time setup:
    python seed.py

This imports the supplied CSV into MySQL and creates a demo farmer.

Demo login:
    Kisan ID: KISAN001
    Password: farmer123

Change the password before real deployment.
"""

import csv
from app import create_app, db
from models import Farmer, Product
from config import Config


def import_products():
    app = create_app()

    with app.app_context():
        if Product.query.count() == 0:
            with open(Config.DATASET_PATH, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    db.session.add(Product(
                        efficientnet_class=row["efficientnet_class"].strip(),
                        crop=row["crop"].strip(),
                        disease=row["disease"].strip(),
                        medicine=row["medicine"].strip(),
                        active_ingredient=row["active_ingredient"].strip(),
                        treatment_type=row["treatment_type"].strip(),
                        description=row["description"].strip(),
                        price=row["price"].strip(),
                    ))
            db.session.commit()
            print("Imported CSV products.")
        else:
            print("Products already exist; skipping import.")

        farmer = Farmer.query.filter_by(kisan_id="KISAN001").first()
        if not farmer:
            farmer = Farmer(kisan_id="KISAN001", name="Demo Farmer")
            farmer.set_password("farmer123")
            db.session.add(farmer)
            db.session.commit()
            print("Created demo farmer: KISAN001 / farmer123")
        else:
            print("Demo farmer already exists.")


if __name__ == "__main__":
    import_products()

# PlantFarma — Flask + MySQL + DocKenny

A Flask agricultural pharmaceutical/pesticide e-commerce application built around the supplied treatment CSV and EfficientNetB0 `.keras` model.

## Features

- Farmer/Kisan ID + password login
- Pesticide catalogue
- Search by medicine, crop, disease, active ingredient, treatment type or EfficientNet class
- Product details
- Add to cart
- Checkout with **Purchased — Confirm Order** button
- Order history
- Order tracking
- DocKenny leaf-image disease detection
- Clickable recommended product bar instead of displaying raw JSON
- MySQL database

## Project structure

```text
pharma_ecommerce/
├── app.py
├── config.py
├── models.py
├── seed.py
├── requirements.txt
├── README.md
├── model/
│   ├── __init__.py
│   ├── disease_detection.py
│   ├── class_labels.json
│   └── plant_disease_efficientnetb0.keras
├── data/
│   └── pesticides.csv
├── database/
│   └── schema.sql
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── products.py
│   ├── cart.py
│   ├── orders.py
│   └── disease.py
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── home.html
│   ├── products.html
│   ├── product_details.html
│   ├── cart.html
│   ├── checkout.html
│   ├── orders.html
│   ├── tracking.html
│   └── disease_detection.html
└── static/
    ├── css/style.css
    ├── js/app.js
    └── uploads/
```

## 1. Install MySQL

Create the database:

```sql
SOURCE database/schema.sql;
```

The default connection is:

- Host: `localhost`
- Port: `3306`
- User: `root`
- Password: `varshit2004`
- Database: `plantfarma`

For real deployment, set these using environment variables instead of keeping passwords in source code.

## 2. Create Python environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Import the supplied CSV

Run:

```bash
python seed.py
```

This imports all rows from `data/pesticides.csv`.

It also creates a demo account:

```text
Kisan ID: KISAN001
Password: farmer123
```

Change this for actual use.

## 4. Start Flask

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## 5. DocKenny model note

The supplied model was inspected as a Keras model and has:

```text
Input: 224 x 224 x 3
Output: 80 softmax classes
```

The `.keras` file does not contain class-name metadata. Therefore `model/class_labels.json` is maintained separately.

The treatment CSV contains 71 `efficientnet_class` mappings. The generated labels file contains those 71 actual CSV class names plus 9 explicit unmapped placeholders.

### Important

The order of class labels must match the order used while training the model.

If you have the original training code/dataset class-index mapping, replace `model/class_labels.json` with the exact 80-class order. Do not reorder labels based on the CSV unless that was also the training-time class order.

The application will still run if a model prediction lands on one of the unmapped 9 classes, but DocKenny will report that no treatment row is mapped for that class.

## DocKenny user experience

The raw internal prediction is never displayed as JSON.

Instead:

```text
Leaf image
   ↓
EfficientNetB0
   ↓
Disease + confidence
   ↓
Find matching CSV/MySQL product
   ↓
Clickable recommended product bar
   ↓
Product details
   ↓
Add to Cart
```

Example UI:

```text
┌─────────────────────────────────────┐
│ Recommended product                 │
│                                     │
│ 🧪 Tilt                             │
│ Fungicide · Propiconazole           │
│                                  →  │
└─────────────────────────────────────┘
```

Clicking the bar opens the product detail page.

## Production notes

This is a complete academic/project prototype. Before real-world pharmaceutical/agricultural-chemical deployment, add:

- HTTPS
- CSRF protection
- production secret management
- proper farmer registration/identity verification
- admin role and admin-only order status updates
- payment gateway
- inventory/stock management
- audit logging
- secure image handling
- rate limiting
- validated regulatory/product information
- appropriate safety and usage warnings

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    MYSQL_USER = os.getenv("MYSQL_USER", "avnadmin")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "AVNS_0FWlV26cWRk9UnHocgo")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "plantfarma-db-vorlaspn1981-bc35.g.aivencloud.com")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "27616")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "defaultdb")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads")
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    MODEL_PATH = str(BASE_DIR / "model" / "plant_disease_efficientnetb0.keras")
    LABELS_PATH = str(BASE_DIR / "model" / "class_labels.json")
    DATASET_PATH = str(BASE_DIR / "data" / "pesticides.csv")

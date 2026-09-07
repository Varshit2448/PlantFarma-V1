import json
import os

import numpy as np
import tensorflow as tf
from PIL import Image


class DiseaseDetector:
    """
    DocKenny disease detector.

    Uses:
        - EfficientNetB0 .keras model
        - class_names.json for model-index -> disease-class mapping

    The model expects:
        (224, 224, 3)

    Important:
        The image is NOT divided by 255 here.
        This follows the original testing code and the supplied
        EfficientNet model's preprocessing.
    """

    def __init__(self, model_path, labels_path):
        self.model_path = model_path
        self.labels_path = labels_path

        self.model = None
        self.class_names = None

        self._load_class_names()

    # ------------------------------------------------------------
    # LOAD CLASS NAMES
    # ------------------------------------------------------------

    def _load_class_names(self):
        if not os.path.exists(self.labels_path):
            raise FileNotFoundError(
                f"Class names file not found:\n{self.labels_path}"
            )

        print("Loading class names...")

        with open(self.labels_path, "r", encoding="utf-8") as f:
            self.class_names = json.load(f)

        print("Class names loaded successfully!")

    # ------------------------------------------------------------
    # LOAD MODEL
    # ------------------------------------------------------------

    def _load_model(self):
        if self.model is not None:
            return

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Disease detection model not found:\n{self.model_path}"
            )

        print("Loading disease detection model...")

        self.model = tf.keras.models.load_model(
            self.model_path,
            compile=False
        )

        print("Model loaded successfully!")

    # ------------------------------------------------------------
    # GET CLASS NAME
    # ------------------------------------------------------------

    def _get_class_name(self, predicted_index):
        """
        Supports both:

        [
            "Apple___Apple_scab",
            "Apple___Black_rot",
            ...
        ]

        and:

        {
            "0": "Apple___Apple_scab",
            "1": "Apple___Black_rot",
            ...
        }
        """

        if isinstance(self.class_names, dict):
            key = str(predicted_index)

            if key not in self.class_names:
                return f"__UNMAPPED_CLASS_{predicted_index:02d}__"

            return self.class_names[key]

        if isinstance(self.class_names, list):
            if predicted_index >= len(self.class_names):
                return f"__UNMAPPED_CLASS_{predicted_index:02d}__"

            return self.class_names[predicted_index]

        raise ValueError(
            "class_names.json must contain either a list or dictionary."
        )

    # ------------------------------------------------------------
    # PREDICT DISEASE
    # ------------------------------------------------------------

    def predict(self, image_path):

        self._load_model()

        # --------------------------------------------------------
        # Load image
        # --------------------------------------------------------

        image = Image.open(
            image_path
        ).convert("RGB")

        # --------------------------------------------------------
        # Resize image for EfficientNetB0
        # --------------------------------------------------------

        image_resized = image.resize(
            (224, 224)
        )

        # --------------------------------------------------------
        # Convert image to NumPy array
        # --------------------------------------------------------

        image_array = np.array(
            image_resized,
            dtype=np.float32
        )

        # --------------------------------------------------------
        # Add batch dimension
        #
        # Shape:
        # (224, 224, 3)
        #
        # becomes:
        # (1, 224, 224, 3)
        # --------------------------------------------------------

        image_array = np.expand_dims(
            image_array,
            axis=0
        )

        # --------------------------------------------------------
        # Model prediction
        # --------------------------------------------------------

        predictions = self.model.predict(
            image_array,
            verbose=0
        )

        # --------------------------------------------------------
        # Get predicted class index
        # --------------------------------------------------------

        predicted_index = int(
            np.argmax(predictions[0])
        )

        # --------------------------------------------------------
        # Get confidence
        # --------------------------------------------------------

        confidence = float(
            predictions[0][predicted_index]
        )

        # --------------------------------------------------------
        # Get disease class using class_names.json
        # --------------------------------------------------------

        disease_class = self._get_class_name(
            predicted_index
        )

        # --------------------------------------------------------
        # Convert disease class to readable name
        # --------------------------------------------------------

        readable_disease = self._readable_disease(
            disease_class
        )

        # --------------------------------------------------------
        # Return internal result
        # --------------------------------------------------------

        return {
            "efficientnet_class": disease_class,
            "confidence": round(confidence * 100, 2),
            "disease": readable_disease,
            "predicted_index": predicted_index
        }

    # ------------------------------------------------------------
    # READABLE DISEASE NAME
    # ------------------------------------------------------------

    @staticmethod
    def _readable_disease(disease_class):

        if disease_class.startswith("__UNMAPPED_CLASS_"):
            return "Unknown disease class"

        # Standard PlantVillage-style format:
        #
        # Apple___Apple_scab
        #
        # Corn_(maize)___Common_rust

        if "___" in disease_class:

            crop, disease_name = disease_class.split(
                "___",
                1
            )

            crop = crop.replace(
                "_",
                " "
            )

            disease_name = disease_name.replace(
                "_",
                " "
            )

            return f"{crop} — {disease_name}"

        # Fallback
        return disease_class.replace(
            "_",
            " "
        )
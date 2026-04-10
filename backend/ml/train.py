import pickle
import logging
from pathlib import Path

import mlflow
import mlflow.sklearn
from codecarbon import EmissionsTracker

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


# =========================
# LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

# Optionnel : réduit le bruit CodeCarbon
logging.getLogger("codecarbon").setLevel(logging.ERROR)


# =========================
# PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parent          # backend/ml
PROJECT_DIR = BASE_DIR.parent                       # backend

MODEL_DIR = PROJECT_DIR / "model"
MODEL_PATH = MODEL_DIR / "model.pkl"

MLFLOW_DB = PROJECT_DIR / "mlflow.db"
ARTIFACT_DIR = PROJECT_DIR / "mlartifacts"

EMISSIONS_FILE = BASE_DIR / "emissions.csv"


# =========================
# MLFLOW CONFIG
# =========================
TRACKING_URI = f"sqlite:///{MLFLOW_DB}"
mlflow.set_tracking_uri(TRACKING_URI)


def train():
    logger.info("Tracking URI = %s", mlflow.get_tracking_uri())

    iris = load_iris()
    X, y = iris.data, iris.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    mlflow.set_experiment("iris-classification")
    mlflow.sklearn.autolog(log_models=False)

    tracker = EmissionsTracker(
        project_name="iris-training",
        output_dir=str(BASE_DIR),
        output_file="emissions.csv",
        gpu_ids=[]  # désactive GPU tracking pour éviter warnings inutiles
    )

    with mlflow.start_run(run_name="RandomForest-iris"):

        tracker.start()

        try:
            params = {
                "n_estimators": 100,
                "max_depth": 5,
                "random_state": 42
            }

            model = RandomForestClassifier(**params)
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="weighted")

            mlflow.log_params(params)
            mlflow.log_metric("test_accuracy", acc)
            mlflow.log_metric("test_f1", f1)

            logger.info("Accuracy=%.4f | F1=%.4f", acc, f1)

            MODEL_DIR.mkdir(parents=True, exist_ok=True)

            with open(MODEL_PATH, "wb") as f:
                pickle.dump(model, f)

            mlflow.log_artifact(str(MODEL_PATH), artifact_path="model")

        finally:
            emissions = tracker.stop()

        logger.info("CO₂ émis : %.8f kg", emissions)

        mlflow.log_metric("carbon_emissions_kg", emissions)

        if EMISSIONS_FILE.exists():
            logger.info("CSV CodeCarbon trouvé : %s", EMISSIONS_FILE)
            mlflow.log_artifact(str(EMISSIONS_FILE), artifact_path="codecarbon")
        else:
            logger.warning("CSV CodeCarbon introuvable : %s", EMISSIONS_FILE)

    print("Tracking URI:", mlflow.get_tracking_uri())
    print("DB exists:", MLFLOW_DB.exists())
    print("CSV exists:", EMISSIONS_FILE.exists())
    print("CSV path:", EMISSIONS_FILE)


if __name__ == "__main__":
    train()
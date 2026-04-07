import os
import pickle
import logging
import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")


def train():
    logger.info("Chargement du dataset Iris...")
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    mlflow.set_experiment("iris-classification")

    mlflow.sklearn.autolog(log_models=False)

    with mlflow.start_run(run_name="RandomForest-iris"):
        params = {"n_estimators": 100, "max_depth": 5, "random_state": 42}
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")

        mlflow.log_metric("test_accuracy", acc)
        mlflow.log_metric("test_f1", f1)
        logger.info(f"Accuracy={acc:.4f}  F1={f1:.4f}")

        os.makedirs(MODEL_DIR, exist_ok=True)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)
        logger.info(f"Modèle sauvegardé : {os.path.abspath(MODEL_PATH)}")

        mlflow.log_artifact(MODEL_PATH, artifact_path="model-pkl")


if __name__ == "__main__":
    train()

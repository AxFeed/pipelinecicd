import os
import sys
import pickle

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict_setosa():
    r = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert r.status_code == 200
    body = r.json()
    assert body["label"] == "setosa"
    assert body["prediction"] == 0


def test_predict_virginica():
    r = client.post("/predict", json={"features": [6.7, 3.0, 5.2, 2.3]})
    assert r.status_code == 200
    assert r.json()["label"] in ["versicolor", "virginica"]


def test_predict_wrong_nb_features():
    r = client.post("/predict", json={"features": [1.0, 2.0]})
    assert r.status_code == 422


def test_model_loadable_and_predicts():
    model_path = os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")
    assert os.path.exists(model_path), "model.pkl doit être présent"
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    pred = model.predict([[5.1, 3.5, 1.4, 0.2]])
    assert pred[0] in [0, 1, 2]

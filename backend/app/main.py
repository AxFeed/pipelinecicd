import os
import pickle
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

MODEL_PATH = os.getenv(
    "MODEL_PATH", os.path.join(os.path.dirname(__file__), "..", "model", "model.pkl")
)

IRIS_CLASSES = ["setosa", "versicolor", "virginica"]
_model = None


def load_model():
    global _model
    path = os.path.abspath(MODEL_PATH)
    logger.info(f"Chargement du modèle depuis : {path}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Modèle introuvable : {path}")
    with open(path, "rb") as f:
        _model = pickle.load(f)
    logger.info("Modèle chargé avec succès")
    return _model


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        load_model()
    except FileNotFoundError as e:
        logger.warning(f"Modèle non trouvé au démarrage : {e}")
    yield


app = FastAPI(title="Iris Classifier API", version="1.0.0", lifespan=lifespan)


class PredictRequest(BaseModel):
    features: List[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="[sepal_length, sepal_width, petal_length, petal_width]",
        examples=[[5.1, 3.5, 1.4, 0.2]],
    )


class PredictResponse(BaseModel):
    prediction: int
    label: str
    features: List[float]


@app.get("/", tags=["health"])
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse, tags=["inference"])
def predict(request: PredictRequest):
    global _model
    if _model is None:
        try:
            load_model()
        except FileNotFoundError as e:
            raise HTTPException(status_code=503, detail=str(e))

    prediction = int(_model.predict([request.features])[0])
    label = IRIS_CLASSES[prediction]
    logger.info(f"Prédiction : {request.features} → {label} (classe {prediction})")
    return PredictResponse(
        prediction=prediction, label=label, features=request.features
    )

import os
import logging
import requests
import streamlit as st

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Iris Classifier", page_icon="🌸", layout="centered")
st.title("🌸 Iris Flower Classifier Les filles en face de moi sont parfaites")
st.markdown("Entrez les mesures de la fleur pour obtenir une prédiction.")

col1, col2 = st.columns(2)
with col1:
    sepal_length = st.number_input("Longueur sépale (cm)", 0.0, 10.0, 5.1, 0.1)
    sepal_width  = st.number_input("Largeur sépale (cm)",  0.0, 10.0, 3.5, 0.1)
with col2:
    petal_length = st.number_input("Longueur pétale (cm)", 0.0, 10.0, 1.4, 0.1)
    petal_width  = st.number_input("Largeur pétale (cm)",  0.0, 10.0, 0.2, 0.1)

if st.button("🔍 Prédire", type="primary"):
    url = f"{BACKEND_URL}/predict"
    payload = {"features": [sepal_length, sepal_width, petal_length, petal_width]}
    logger.info(f"Appel POST {url} avec {payload}")
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        result = r.json()
        st.success(f"**Espèce prédite : {result['label'].capitalize()}** (classe {result['prediction']})")
    except requests.exceptions.ConnectionError:
        st.error(f"Backend inaccessible ({url}). Vérifiez que l'API est démarrée.")
    except requests.exceptions.HTTPError as e:
        st.error(f"Erreur API ({r.status_code}) : {r.json().get('detail', str(e))}")
    except Exception as e:
        st.error(f"Erreur inattendue : {e}")
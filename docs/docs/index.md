# Iris CI/CD Project

Démonstration complète d'un pipeline CI/CD incluant :

- **Modèle ML** : RandomForest sur le dataset Iris, suivi avec MLflow 3.x
- **API** : FastAPI 0.135+ avec Pydantic v2
- **Frontend** : Streamlit
- **CI/CD** : GitHub Actions → DockerHub → Azure App Service

## Lancer en local
```bash
# Entraîner le modèle
python backend/ml/train.py

# Lancer l'API
fastapi dev backend/app/main.py

# Lancer le frontend
streamlit run frontend/app.py
```
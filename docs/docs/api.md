# API — Iris Classifier

L'API est construite avec **FastAPI 0.135+** et expose deux routes.  
La documentation interactive est disponible automatiquement à `/docs` (Swagger UI) et `/redoc`.

---

## Routes

### `GET /`

Vérifie que l'API est en vie.

**Réponse**
```json
{ "status": "ok" }
```

---

### `POST /predict`

Effectue une prédiction sur les 4 features de la fleur Iris.

**Corps de la requête**
```json
{
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

| Champ      | Type            | Description                                                              |
|------------|-----------------|--------------------------------------------------------------------------|
| `features` | `list[float]`   | Exactement 4 valeurs : sepal_length, sepal_width, petal_length, petal_width |

**Réponse**
```json
{
  "prediction": 0,
  "label": "setosa",
  "features": [5.1, 3.5, 1.4, 0.2]
}
```

| Champ        | Type          | Description                          |
|--------------|---------------|--------------------------------------|
| `prediction` | `int`         | Classe prédite (0, 1 ou 2)           |
| `label`      | `str`         | Nom de l'espèce (`setosa`, `versicolor`, `virginica`) |
| `features`   | `list[float]` | Features reçues en entrée            |

**Codes d'erreur**

| Code | Cause                                          |
|------|------------------------------------------------|
| 422  | Mauvais nombre de features (pas exactement 4)  |
| 503  | Modèle non trouvé au démarrage                 |

---

## Lancer l'API en local

```bash
# Depuis la racine du projet
python backend/ml/train.py          # génère backend/model/model.pkl
uvicorn backend.app.main:app --reload --port 8000
```

Puis ouvrir [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Lancer avec Docker

```bash
docker build -t iris-backend ./backend
docker run -p 8000:8000 iris-backend
```

---

## Variables d'environnement

| Variable     | Défaut                          | Description                     |
|--------------|---------------------------------|---------------------------------|
| `MODEL_PATH` | `../model/model.pkl` (relatif)  | Chemin absolu vers le fichier `.pkl` |

Le chemin est résolu avec `os.path.abspath` au démarrage — il fonctionne en local, en Docker et sur Azure sans modification du code.

# Pipeline CI/CD

Le pipeline est défini dans `.github/workflows/ci.yml` et se déclenche à chaque **push sur la branche `main`**.

---

## Vue d'ensemble

```
push sur main
     │
     ▼
┌─────────────────────────────────┐
│  1. Checkout du code            │
│  2. Setup Python 3.11           │
│  3. Install dépendances backend │
│  4. Entraînement du modèle      │
│  5. Tests (pytest)              │
│  6. Déploiement documentation   │
│  7. Build image backend         │
│  8. Build image frontend        │
│  9. Push images → DockerHub     │
└─────────────────────────────────┘
     │
     ▼
Azure App Service (déploiement continu)
```

---

## Étapes détaillées

### 1. Checkout
```yaml
- uses: actions/checkout@v4
```
Récupère le code source du repo dans le runner Ubuntu.

---

### 2. Setup Python
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.11"
```

---

### 3 & 4. Dépendances + entraînement du modèle
Le modèle `.pkl` n'est pas versionné dans Git. Il est donc entraîné à chaque run **avant** les tests pour que ceux-ci puissent le charger.

```yaml
- run: pip install -r backend/requirements.txt
- run: python backend/ml/train.py
```

---

### 5. Tests
```yaml
- run: pytest backend/tests/ -v
```

4 tests couvrent : le health check, deux prédictions, la validation des inputs et le chargement du `.pkl`.

---

### 6. Documentation
```yaml
- run: pip install mkdocs-material
- run: mkdocs gh-deploy --force --config-file docs/mkdocs.yml
```

La doc est déployée sur **GitHub Pages** (branche `gh-pages`).  
Prérequis : dans Settings → Actions → General → activer **Read and write permissions**.

---

### 7–9. Docker
```yaml
- uses: docker/login-action@v3        # connexion DockerHub via secrets
- uses: docker/build-push-action@v6   # build + push backend
- uses: docker/build-push-action@v6   # build + push frontend
```

Les images sont taguées `:latest` et poussées sur DockerHub :

- `<username>/iris-backend:latest`
- `<username>/iris-frontend:latest`

Le cache GHA (`cache-from: type=gha`) accélère les builds successifs.

---

## Secrets requis

À configurer dans **Settings → Secrets and variables → Actions** :

| Secret               | Valeur                            |
|----------------------|-----------------------------------|
| `DOCKERHUB_USERNAME` | Votre nom d'utilisateur DockerHub |
| `DOCKERHUB_TOKEN`    | Personal Access Token (Read & Write) |

---

## Ajouter ruff (bonus)

Pour vérifier le formatage du code, ajouter cette étape avant les tests :

```yaml
- name: Lint with ruff
  run: |
    pip install ruff
    ruff check backend/
```

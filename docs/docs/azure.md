# Déploiement Azure

Le déploiement repose sur **Azure App Service** avec des conteneurs Docker tirés depuis DockerHub.  
Une fois configuré, chaque push sur `main` met à jour automatiquement les apps via le déploiement continu.

---

## Prérequis

- Pipeline CI/CD fonctionnel (images poussées sur DockerHub)
- Compte Azure actif
- Les secrets `DOCKERHUB_USERNAME` et `DOCKERHUB_TOKEN` configurés dans GitHub

---

## Création des App Services

Répéter l'opération pour le **backend** puis le **frontend**.

1. Portail Azure → **Créer une ressource** → **Application web**
2. Remplir les champs :
    - **Région** : France centrale
    - **Publication** : Conteneur
    - **Système d'exploitation** : Linux
3. Onglet **Conteneur** :
    - Source : Docker Hub
    - Type d'accès : Public
    - Image : `<username>/iris-backend:latest` (ou `iris-frontend:latest`)
4. Valider et créer.

---

## Configuration du backend

### Port exposé
Dans l'app backend → **Paramètres** → **Configuration** → onglet **Général** :

- Port de conteneur : `8000`

### Vérification
Accéder à `https://<url-backend>.azurewebsites.net/docs` — la Swagger UI doit s'afficher.

---

## Configuration du frontend

### Variable d'environnement
Dans l'app frontend → **Paramètres** → **Variables d'environnement** → ajouter :

| Nom           | Valeur                                            |
|---------------|---------------------------------------------------|
| `BACKEND_URL` | `https://<url-backend>.azurewebsites.net`         |

### Port exposé
Port de conteneur : `8501`

---

## Déploiement continu

Pour chaque app (backend et frontend) :

1. **Deployment Center** → cocher **Continuous deployment** sur le conteneur principal
2. Azure surveille DockerHub : dès qu'une nouvelle image `:latest` est poussée, l'app redémarre automatiquement.

Le flux complet devient :
```
git push main → CI → DockerHub → Azure (auto-redémarrage)
```

---

## Tester le déploiement

```bash
# Health check backend
curl https://<url-backend>.azurewebsites.net/

# Prédiction
curl -X POST https://<url-backend>.azurewebsites.net/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

Le frontend Streamlit est accessible à `https://<url-frontend>.azurewebsites.net`.

---

## Dépannage

| Symptôme | Cause probable | Solution |
|----------|---------------|----------|
| `/predict` retourne 503 | Modèle `.pkl` absent de l'image | Ajouter `RUN python ml/train.py` dans le Dockerfile backend |
| Frontend ne joint pas le backend | `BACKEND_URL` manquant ou erroné | Vérifier la variable d'env dans l'app frontend |
| App ne démarre pas | Mauvais port configuré | Vérifier le port dans Configuration → Général |
| Image non mise à jour | Déploiement continu désactivé | Vérifier Deployment Center |

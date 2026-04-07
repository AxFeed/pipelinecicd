# Iris CI/CD Project

Car le déploiement c'est super

## Entrainement de model

On commence par entrainer notre model en utilisant le dataset Iris disponible dans la bibliothèque sklearn.

```py 
from sklearn.datasets import load_iris
```

On utilise aussi mlflow en autolog pour tout log de l'entrainement.
Ensuite je l'utilise pour entrainer mon model (ici j'ai fais un randomForest)
Dès que l'entrainement est fini j'enregistre le fichier .pkl à l'endroit de mon choix

## API

Je charge mon model puis je créer mes routes pour faire la prédiction avec mon model.
Je m'assure ensuite après avoir lancer mon API que mes routes fonctionnent.

## Front

Je créer mon front qui fais des appels à l'API pour faire la prédiction avec ce que l'utilisateur envoie. Puis affiche le résultat.

## Test en python

Je fais des tests en envoyant des requêtes à mon API dont je connais la réponse, j'attend donc le retour et je vérifie avec assert que c'est bien la réponse que j'attends.

```py
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
```

Après pytest test_api.py et si il n'y a pas d'erreur c'est que mon API marche comme il faut. (Théoriquement il faudrait écrire les tests avec les fonctions de l'API)

## Dockerfile & Docker compose

On va créer deux dockerfile, un pour le Front et l'autre pour le Back.
Donc on sait comme d'habitude, quel python on utilise, le workspace de travail, ou est ce qu'on stocke notre model ect...
Pareil on fait le docker compose

## Fichier de deploiement Github

Ici on commence à lui dire le nom de notre déploiement et sur quelle action il se lancera.
On lui donne aussi les permissions dont il a besoin.

Arrive ensuite le travail qu'il va devoir effectuer :
- Installer Python
- Installer les dépendances du front et du back
- Lancer le train.py pour entrainer le model
- Utiliser Ruff pour formatter et fix les éventuels problèmes de code
- Lancer les tests de pytest
- Déployer la documentation
- Se log sur DockerHub (On en a besoin pour mettre nos docker en ligne pour ensuite les utiliser via Azure) ===> ATTENTION SE REFERER A LA FIN DE LA LISTE
- Push la partie backend sur DockerHub en lui donnant un bon nom
- Push la partie frontend sur DockerHub en lui donnant un bon nom

Pour que ce soit directement plus simple dans notre script de déploiement dans "Settings" de notre projet on peut rentrer des "secrets" c'est comme un .env dans github. Un genre de dictionnaire Clé/Valeur.
Ici on veut stocker notre nom d'utilisateur DockerHub et le token privé de notre compte DockerHub.

## Azure

Pour déployer sur Azure, on va sur le Azure Portal puis on cherche "Azure Web App", on lui donne un nom et on publie en tant que Docker en France Centrale.
Après avoir fait ça dans la section Conteneur, on prend "Autres registres de conteneurs", le nom qu'on veut, URL de serveur de registre on laisse https://index.docker.io, puis pour Image et étiquette vous mettez NomUtilisateurDockerHub/leNomQueVousAviezDonnerPourLimageSurLeWorkflowGithub:lastest. Et en port 8000 (API) et 8501 (Front).
Dès que c'est fait vous pouvez vérifier et créer.

ATTENTION, pour la partie Frontend, il faudra aller dans la ressource, puis "Parametres" et dans Variable d'environnement il faudra créer une nouvelle variable BACKEND_URL, et on met l'URL de la ressource de l'API.



Voilà finito pipo



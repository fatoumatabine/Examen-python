# API RESTful - Gestion des Approvisionnements

API développée avec Flask (Python) pour gérer les fournisseurs, produits et approvisionnements d'une boutique.

## 🚀 Installation

### 1. Cloner le projet
```bash
git clone https://github.com/fatoumatabine/Examen-python.git
cd Examen-python
```

### 2. Environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration PostgreSQL (optionnel)

**Par défaut** : SQLite (fichier `app.db` créé automatiquement).

**Pour utiliser PostgreSQL** :

1. Installez PostgreSQL :
```bash
sudo apt-get install postgresql postgresql-contrib
```

2. Démarrez le service :
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

3. Créez un utilisateur et une base de données :
```bash
sudo -u postgres psql
CREATE USER gest_user WITH PASSWORD 'votre_mot_de_passe';
CREATE DATABASE gest_db OWNER gest_user;
GRANT ALL PRIVILEGES ON DATABASE gest_db TO gest_user;
\q
```

4. Modifiez `app/config.py` ou définissez la variable d'environnement :
```bash
export DATABASE_URL="postgresql://gest_user:votre_mot_de_passe@localhost:5432/gest_db"
```

Ou ajoutez dans `.env` :
```
DATABASE_URL=postgresql://gest_user:votre_mot_de_passe@localhost:5432/gest_db
```

5. Exécutez le script d'initialisation (optionnel) :
```bash
python init_postgres.py
```

### 5. Configuration Cloudinary (pour upload d'images)

Créez un compte sur Cloudinary et récupérez vos credentials.

Ajoutez dans `.env` :
```
CLOUDINARY_CLOUD_NAME=votre_cloud_name
CLOUDINARY_API_KEY=votre_api_key
CLOUDINARY_API_SECRET=votre_api_secret
CLOUDINARY_FOLDER=gestion-approvisionnements
```

## ▶️ Lancer l'API

```bash
source venv/bin/activate
python main.py
```

L'API est accessible sur : **http://127.0.0.1:5002**

## 📚 Documentation Swagger

Interface interactive de documentation :
- http://127.0.0.1:5002/apidocs

## 🔐 Authentification

1. Créer un utilisateur :
```bash
curl -X POST http://127.0.0.1:5002/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nom":"Admin","email":"admin@example.com","password":"1234"}'
```

2. Se connecter :
```bash
curl -X POST http://127.0.0.1:5002/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"1234"}'
```

3. Utiliser le token (remplacez `<VOTRE_TOKEN>`):
```bash
curl -H "Authorization: Bearer <VOTRE_TOKEN>" \
  http://127.0.0.1:5002/api/produits
```

## 📦 Endpoints API

### Authentification
- `POST /api/auth/register` — Créer un compte
- `POST /api/auth/login` — Connexion
- `GET /api/auth/me` — Infos utilisateur connecté

### Fournisseurs
- `GET /api/fournisseurs` — Liste tous
- `POST /api/fournisseurs` — Créer
- `GET /api/fournisseurs/:id` — Récupérer un
- `PUT /api/fournisseurs/:id` — Modifier
- `DELETE /api/fournisseurs/:id` — Supprimer

### Produits
- `GET /api/produits` — Liste tous
- `POST /api/produits` — Créer
- `GET /api/produits/:id` — Récupérer un
- `PUT /api/produits/:id` — Modifier
- `DELETE /api/produits/:id` — Supprimer
- `POST /api/produits/:id/image` — Upload image (Cloudinary)
- `PATCH /api/produits/:id/increment` — Augmenter stock
- `PATCH /api/produits/:id/decrement` — Diminuer stock

### Approvisionnements
- `GET /api/approvisionnements` — Liste tous
- `POST /api/approvisionnements` — Créer (incrémente stock automatiquement)

## 🧪 Tests rapides

```bash
# Santé
curl http://127.0.0.1:5002/api/health

# Créer un fournisseur (après login)
curl -X POST http://127.0.0.1:5002/api/fournisseurs \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nom":"XYZ Corp","telephone":"771234567","adresse":"Dakar"}'

# Créer un produit
curl -X POST http://127.0.0.1:5002/api/produits \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"libelle":"Laptop","prixUnitaire":500000}'

# Upload image
curl -X POST http://127.0.0.1:5002/api/produits/1/image \
  -H "Authorization: Bearer TOKEN" \
  -F "image=@chemin/vers/image.jpg"
```

## 🗄️ Structure du projet

```
gest_python/
├── app/
│   ├── __init__.py          # Initialisation Flask, blueprints, Swagger
│   ├── config.py            # Configuration (DB, Cloudinary, JWT)
│   ├── models.py            # Modèles SQLAlchemy (User, Fournisseur, Produit, Approvisionnement)
│   ├── middlewares/
│   │   └── auth_middleware.py  # Authentification JWT
│   └── routes/
│       ├── auth_routes.py       # /api/auth/*
│       ├── fournisseur_routes.py # /api/fournisseurs/*
│       ├── produit_routes.py     # /api/produits/*
│       └── approvisionnement_routes.py # /api/approvisionnements/*
├── main.py                  # Point d'entrée
├── requirements.txt         # Dépendances
├── swagger.yml             # Documentation OpenAPI
├── .env                    # Variables d'environnement
└── init_postgres.py        # Script init PostgreSQL
```

## ⚙️ Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `SECRET_KEY` | Clé secrète Flask | `dev-secret-key` |
| `DATABASE_URL` | Connection string DB | `postgresql://...` ou `sqlite:///app.db` |
| `JWT_SECRET` | Clé secrète JWT | `jwt-secret-key` |
| `CLOUDINARY_CLOUD_NAME` | Cloudinary cloud name | `''` |
| `CLOUDINARY_API_KEY` | Cloudinary API key | `''` |
| `CLOUDINARY_API_SECRET` | Cloudinary API secret | `''` |
| `CLOUDINARY_FOLDER` | Dossier Cloudinary | `gestion-approvisionnements` |

## 📝 Notes

- Toutes les routes (sauf `/api/health` et auth) nécessitent un token JWT.
- Le stock ne peut pas devenir négatif (vérifié sur decrement).
- L'upload d'image stocke le lien sur Cloudinary.
- L'approvisionnement incrémente automatiquement le stock du produit.

## 🔄 Commandes Git

```bash
git add .
git commit -m "message"
git push -u origin main
```

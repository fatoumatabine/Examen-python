-- Créer la base de données
CREATE DATABASE IF NOT EXISTS gest_db;

-- Se connecter à la base de données
\c gest_db;

-- Les tables seront créées automatiquement par SQLAlchemy
-- (modèle User, Fournisseur, Produit, Approvisionnement dans app/models.py)

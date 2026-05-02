from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Fournisseur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(100), nullable=False)
    prix_unitaire = db.Column(db.Float, nullable=False)
    quantite_en_stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))
    image_public_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Approvisionnement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    quantite = db.Column(db.Integer, nullable=False)
    fournisseur_id = db.Column(db.Integer, db.ForeignKey('fournisseur.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    fournisseur = db.relationship('Fournisseur', backref='approvisionnements')
    produit = db.relationship('Produit', backref='approvisionnements')
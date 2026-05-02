from flask import Blueprint, request, jsonify
from app import db
from app.models import Fournisseur
from app.middlewares.auth_middleware import authenticate

fournisseur_bp = Blueprint('fournisseur', __name__)

@fournisseur_bp.route('', methods=['GET'])
@authenticate
def get_fournisseurs():
    fournisseurs = Fournisseur.query.all()
    return jsonify([{'id': f.id, 'nom': f.nom, 'telephone': f.telephone, 'adresse': f.adresse} for f in fournisseurs])

@fournisseur_bp.route('/<int:id>', methods=['GET'])
@authenticate
def get_fournisseur(id):
    fournisseur = Fournisseur.query.get_or_404(id)
    return jsonify({'id': fournisseur.id, 'nom': fournisseur.nom, 'telephone': fournisseur.telephone, 'adresse': fournisseur.adresse})

@fournisseur_bp.route('', methods=['POST'])
@authenticate
def create_fournisseur():
    data = request.get_json()
    fournisseur = Fournisseur(nom=data['nom'], telephone=data['telephone'], adresse=data['adresse'])
    db.session.add(fournisseur)
    db.session.commit()
    return jsonify({'message': 'Fournisseur cree', 'id': fournisseur.id}), 201

@fournisseur_bp.route('/<int:id>', methods=['PUT'])
@authenticate
def update_fournisseur(id):
    fournisseur = Fournisseur.query.get_or_404(id)
    data = request.get_json()
    fournisseur.nom = data.get('nom', fournisseur.nom)
    fournisseur.telephone = data.get('telephone', fournisseur.telephone)
    fournisseur.adresse = data.get('adresse', fournisseur.adresse)
    db.session.commit()
    return jsonify({'message': 'Fournisseur mis a jour'})

@fournisseur_bp.route('/<int:id>', methods=['DELETE'])
@authenticate
def delete_fournisseur(id):
    fournisseur = Fournisseur.query.get_or_404(id)
    db.session.delete(fournisseur)
    db.session.commit()
    return jsonify({'message': 'Fournisseur supprime'})
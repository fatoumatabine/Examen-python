from flask import Blueprint, request, jsonify
from app import db
from app.models import Approvisionnement, Produit
from app.middlewares.auth_middleware import authenticate

approvisionnement_bp = Blueprint('approvisionnement', __name__)

@approvisionnement_bp.route('', methods=['GET'])
@authenticate
def get_approvisionnements():
    approvisionnements = Approvisionnement.query.all()
    return jsonify([{
        'id': a.id,
        'date': a.date.isoformat(),
        'quantite': a.quantite,
        'fournisseurId': a.fournisseur_id,
        'produitId': a.produit_id
    } for a in approvisionnements])

@approvisionnement_bp.route('/<int:id>', methods=['GET'])
@authenticate
def get_approvisionnement(id):
    approvisionnement = Approvisionnement.query.get_or_404(id)
    return jsonify({
        'id': approvisionnement.id,
        'date': approvisionnement.date.isoformat(),
        'quantite': approvisionnement.quantite
    })

@approvisionnement_bp.route('', methods=['POST'])
@authenticate
def create_approvisionnement():
    data = request.get_json()
    produit = Produit.query.get_or_404(data['produitId'])
    
    approvisionnement = Approvisionnement(
        quantite=data['quantite'],
        fournisseur_id=data['fournisseurId'],
        produit_id=data['produitId']
    )
    produit.quantite_en_stock += data['quantite']
    
    db.session.add(approvisionnement)
    db.session.commit()
    return jsonify({'message': 'Approvisionnement cree', 'id': approvisionnement.id}), 201
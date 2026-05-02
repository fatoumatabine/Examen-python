from flask import Blueprint, request, jsonify
from app import db
from app.models import Produit
from app.middlewares.auth_middleware import authenticate
import cloudinary
import cloudinary.uploader
from app.config import Config

cloudinary.config(
    cloud_name=Config.CLOUDINARY_CLOUD_NAME,
    api_key=Config.CLOUDINARY_API_KEY,
    api_secret=Config.CLOUDINARY_API_SECRET
)

produit_bp = Blueprint('produit', __name__)

@produit_bp.route('', methods=['GET'])
@authenticate
def get_produits():
    produits = Produit.query.all()
    return jsonify([{
        'id': p.id,
        'libelle': p.libelle,
        'prixUnitaire': p.prix_unitaire,
        'quantiteEnStock': p.quantite_en_stock,
        'imageUrl': p.image_url,
        'imagePublicId': p.image_public_id
    } for p in produits])

@produit_bp.route('/<int:id>', methods=['GET'])
@authenticate
def get_produit(id):
    produit = Produit.query.get_or_404(id)
    return jsonify({
        'id': produit.id,
        'libelle': produit.libelle,
        'prixUnitaire': produit.prix_unitaire,
        'quantiteEnStock': produit.quantite_en_stock,
        'imageUrl': produit.image_url,
        'imagePublicId': produit.image_public_id
    })

@produit_bp.route('', methods=['POST'])
@authenticate
def create_produit():
    data = request.get_json()
    produit = Produit(libelle=data['libelle'], prix_unitaire=data['prixUnitaire'])
    db.session.add(produit)
    db.session.commit()
    return jsonify({'message': 'Produit cree', 'id': produit.id}), 201

@produit_bp.route('/<int:id>', methods=['PUT'])
@authenticate
def update_produit(id):
    produit = Produit.query.get_or_404(id)
    data = request.get_json()
    if 'libelle' in data:
        produit.libelle = data['libelle']
    if 'prixUnitaire' in data:
        produit.prix_unitaire = data['prixUnitaire']
    db.session.commit()
    return jsonify({'message': 'Produit mis a jour'})

@produit_bp.route('/<int:id>', methods=['DELETE'])
@authenticate
def delete_produit(id):
    produit = Produit.query.get_or_404(id)
    db.session.delete(produit)
    db.session.commit()
    return jsonify({'message': 'Produit supprime'})

@produit_bp.route('/<int:id>/image', methods=['POST'])
@authenticate
def upload_produit_image(id):
    produit = Produit.query.get_or_404(id)

    if 'image' not in request.files:
        return jsonify({'message': 'Aucune image fournie'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'message': 'Aucun fichier selectionne'}), 400

    try:
        upload_result = cloudinary.uploader.upload(
            file,
            folder=Config.CLOUDINARY_FOLDER,
            public_id=f'produit_{id}_{file.filename.rsplit(".", 1)[0]}'
        )

        produit.image_url = upload_result.get('secure_url')
        produit.image_public_id = upload_result.get('public_id')
        db.session.commit()

        return jsonify({
            'message': 'Image telechargee avec succes',
            'imageUrl': produit.image_url,
            'imagePublicId': produit.image_public_id
        }), 200
    except Exception as e:
        return jsonify({'message': f'Erreur lors du telechargement: {str(e)}'}), 500
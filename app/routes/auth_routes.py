from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import create_access_token
from app import db, bcrypt
from app.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('nom'):
        return jsonify({'message': 'Donnees incompletes'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Cet email existe deja'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(nom=data['nom'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Utilisateur cree avec succes'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email et mot de passe requis'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Email ou mot de passe incorrect'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({'token': access_token, 'user': {'id': user.id, 'nom': user.nom, 'email': user.email}})

@auth_bp.route('/me', methods=['GET'])
def me():
    from app.middlewares.auth_middleware import authenticate
    return authenticate(lambda: jsonify({}))
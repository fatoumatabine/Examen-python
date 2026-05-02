from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return jsonify({'message': 'Utilisateur introuvable'}), 401
        except Exception as e:
            return jsonify({'message': 'Acces refuse. Token manquant.'}), 401
        return f(*args, **kwargs)
    return decorated_function
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.produit_routes import produit_bp
    from app.routes.fournisseur_routes import fournisseur_bp
    from app.routes.approvisionnement_routes import approvisionnement_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(produit_bp, url_prefix='/api/produits')
    app.register_blueprint(fournisseur_bp, url_prefix='/api/fournisseurs')
    app.register_blueprint(approvisionnement_bp, url_prefix='/api/approvisionnements')

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'success': True, 'message': 'API operationnelle'})

    return app
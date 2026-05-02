from app import create_app, db
from app.models import User, Fournisseur, Produit, Approvisionnement

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=False, port=5002, use_reloader=False)
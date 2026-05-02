import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 86400

    # Cloudinary config
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME') or ''
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY') or ''
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET') or ''
    CLOUDINARY_FOLDER = os.environ.get('CLOUDINARY_FOLDER') or 'gestion-approvisionnements'
#!/usr/bin/env python3
"""
Script d'initialisation de la base de données PostgreSQL.
À exécuter avant de lancer l'application.
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = 'gest_db'
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')

def create_database():
    try:
        # Connexion à la base postgres pour créer la BD
        conn = psycopg2.connect(
            dbname='postgres',
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Vérifier si la BD existe
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f'CREATE DATABASE {DB_NAME}')
            print(f"✅ Base de données '{DB_NAME}' créée.")
        else:
            print(f"ℹ️  Base de données '{DB_NAME}' existe déjà.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("💡 Assurez-vous que PostgreSQL est installé et en cours d'exécution.")
        print("   sudo systemctl status postgresql")
        print("   ou: sudo service postgresql status")

if __name__ == '__main__':
    create_database()

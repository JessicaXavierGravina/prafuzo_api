from flask import Flask, request, jsonify, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
import os
from decouple import config


app = Flask(__name__)

# Configuração do SQLAlchemy (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
database = SQLAlchemy(app)

# Configuração do MongoDB
MONGO_HOST = config('MONGO_HOST')
MONGO_PORT = config('MONGO_PORT', default=27017, cast=int)
MONGO_USER = config('MONGO_USER')
MONGO_PASSWORD = config('MONGO_PASSWORD')
MONGO_DATABASE = config('MONGO_DATABASE')

if os.getenv('DATABASE_URL'):
    MONGODB_URI = os.getenv('DATABASE_URL')
else:
    MONGODB_URI = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DATABASE}'

# Instância do PyMongo para se conectar ao MongoDB
mongo = MongoClient(MONGODB_URI)
mongo_db = mongo[MONGO_DATABASE]

# try:
#     client = MongoClient(MONGODB_URI)
#     db = client.get_database()
#     print("Conexão com o MongoDB bem-sucedida!")
# except Exception as e:
#     print(f"Erro ao conectar ao MongoDB: {str(e)}")

from api import routes
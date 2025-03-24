import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'supersecretkey'  # Verander dit in een echte geheime sleutel
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'bungalowpark.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

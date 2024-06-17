import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://flaskuser:flaskpassword@db:5432/flaskdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_very_secret_key'
    SESSION_TYPE = 'filesystem'  # To store session data on the server's file system
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://Arunipapers:Hello%402024@catpapers.postgres.database.azure.com:5432/postgres'
from flask import Flask, jsonify
from app.config import get_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(env='development'):
  app = Flask(__name__)
  app.config.from_object(get_config(env))

  db.init_app(app)
  migrate.init_app(app, db)

  
  @app.route('/')
  def health_check() -> dict:  # type: ignore
    return jsonify({
      'status': 'ok',
      'message': 'Flowise Backend is running',
      'environment': env
    })
  
  return app
  

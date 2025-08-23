from flask import Flask, jsonify
from app.config import get_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.core.jwt_config import configure_jwt

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# Import all models so they are registered with SQLAlchemy
from app.models import (
    auth_providers_model,
    daily_report_model,
    project_comment_model,
    project_model,
    time_entry_model,
    user_model,
    user_proyect_model,
    weekly_report_model,
    work_schedule_model
)

def create_app(env='development'):
  app = Flask(__name__)
  app.config.from_object(get_config(env))

  db.init_app(app)
  migrate.init_app(app, db)
  configure_jwt(app)

  # Register blueprints
  from app.routes import auth_routes, profile_routes
  app.register_blueprint(auth_routes.bp)
  app.register_blueprint(profile_routes.bp)

  @app.route('/')
  def health_check() -> dict:  # type: ignore
    return jsonify({
      'status': 'ok',
      'message': 'Flowise Backend is running',
      'environment': env
    })
  
  return app
  

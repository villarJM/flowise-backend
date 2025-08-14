from flask import Flask, jsonify
from app.config import get_config

def create_app(env='development'):
  app = Flask(__name__)
  app.config.from_object(get_config(env))
  
  @app.route('/')
  def health_check() -> dict:  # type: ignore
    return jsonify({
      'status': 'ok',
      'message': 'Flowise Backend is running',
      'environment': env
    })
  
  return app
  

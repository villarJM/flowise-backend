from flask import Blueprint, request
from marshmallow import ValidationError as MarshmallowValidationError
from flask_jwt_extended import jwt_required
from app.schemas.user_login_schema import UserLoginSchema
from app.services.auth_service import AuthService
from app.services.firebase_auth_service import FirebaseAuthService
from app.schemas.user_register_schema import UserRegisterSchema
from app.core.utils.response_utils import create_response
from app.core.exceptions import ValidationError
import os

bp = Blueprint("auth", __name__, url_prefix='/auth')

# Login user
@bp.route("/login", methods=["POST"])
def login():
  # Verificar que el Content-Type sea application/json
  if not request.is_json:
    return create_response("Content-Type must be application/json", 415)

  # Verificar que el cuerpo no esté vacío
  if not request.json:
    return create_response("Request body is empty", 400)

  user_schema = UserLoginSchema()

  try:
    data = user_schema.load(request.json)
  except MarshmallowValidationError as err:
    return create_response("Fields Required", 400, err.messages)

  # Llamar al servicio de autenticación
  try:
    data = AuthService.login_user(data)
  except ValidationError as err:
    return create_response(str(err), err.code)
  except Exception as err:
    return create_response("Login failed", 500, str(err))

  return create_response("Login successful", 200, data)

# Register a new user
@bp.route("/register", methods=["POST"])
def register():
  # Verificar que el Content-Type sea application/json
  if not request.is_json:
    return create_response("Content-Type must be application/json", 415)
  
  # Verificar que el cuerpo no esté vacío
  if not request.json:
    return create_response("Request body is empty", 400)
  
  user_schema = UserRegisterSchema()

  try:
    data = user_schema.load(request.json)
  except MarshmallowValidationError as err:
    return create_response("Fields Invalid", 400, err.messages)

  try:
    user = AuthService.register_user(data)
  except ValidationError as err:
    return create_response(str(err), err.code)
  except Exception as err:
    return create_response("User registration failed", 500, str(err))

  return create_response("User registered successfully", 201, user_schema.dump(user))

# Firebase Authentication
@bp.route("/firebase/login", methods=["POST"])
def firebase_login():
  if not request.is_json:
    return create_response("Content-Type must be application/json", 415)
    
  id_token = request.json.get('id_token')
  if not id_token:
    return create_response("Firebase id_token is required", 400)
  
  try:
    # Verificar token de Firebase
    firebase_user_info = FirebaseAuthService.verify_firebase_token(id_token)
    
    # Crear/actualizar usuario y generar JWT
    result = FirebaseAuthService.create_or_update_user(firebase_user_info)
    
    return create_response("Firebase login successful", 200, result)
    
  except ValidationError as err:
    return create_response(str(err), err.code)
  except Exception as err:
    return create_response("Firebase authentication failed", 500, str(err))

# Logout
@bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
  try:
    result = AuthService.logout_user()
    return create_response("Logout successful", 200, result)
  except Exception as err:
    return create_response("Logout failed", 500, str(err))

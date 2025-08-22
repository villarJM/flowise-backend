from flask import Blueprint, request, jsonify
from marshmallow import ValidationError as MarshmallowValidationError
from app.schemas.user_login_schema import UserLoginSchema
from app.services.auth_service import AuthService
from app.schemas.user_register_schema import UserRegisterSchema
from app.core.utils.response_utils import create_response
from app.core.exceptions import ValidationError

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
    user = AuthService.login_user(data)
  except ValidationError as err:
    return create_response(str(err), err.code)
  except Exception as err:
    return create_response("Login failed", 500, str(err))

  return create_response("Login successful", 200, {
    "id": user.id,
    "email": user.email,
    "name": user.name,
    "role": user.role
  })

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

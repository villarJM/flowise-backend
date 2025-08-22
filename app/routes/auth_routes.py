from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from app.services.auth_service import AuthService
from app.schemas.user_register_schema import UserRegisterSchema
from app.core.utils.response_utils import create_response

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

  # Obtener los datos del cuerpo de la petición
  data = {
    "email": request.json["email"],
    "password": request.json["password"]
  }

  # Llamar al servicio de autenticación
  try:
    user = AuthService.login_user(data)
  except ValidationError as err:
    return create_response("Login failed", 400, err.messages)
  except Exception as err:
    return create_response("Login failed", 500, str(err))

  return create_response("Login successful", 200, user)

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
    user = AuthService.register_user(data)
  except ValidationError as err:
    return create_response("Fields Invalidate", 400, err.messages)
  except Exception as err:
    return create_response(str(err), err.code)

  return create_response("User registered successfully", 201, user_schema.dump(user))

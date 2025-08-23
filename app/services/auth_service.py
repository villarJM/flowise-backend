from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt
from app.repositories.auth_repository import AuthRepository
from app.core.exceptions import ValidationError
import bcrypt
import redis
import os

# Redis client para blacklist
redis_client = redis.Redis(
  host=os.getenv('REDIS_HOST', 'localhost'),
  port=int(os.getenv('REDIS_PORT', 6379)),
  db=int(os.getenv('REDIS_DB', 0)),
  decode_responses=True
)

class AuthService:

  @staticmethod
  def login_user(data: dict[str, any]):
    """Login user"""
    # Check if user exists
    user = AuthRepository.get_user_by_email(data["email"])
    if not user:
      raise ValidationError("User not found", 404)
    # Check if password is correct
    if not AuthService.check_password(data["password"], user.password):
      raise ValidationError("Incorrect password", 401)

    access_token = create_access_token(identity=user.id, fresh=True)
    refresh_token = create_refresh_token(identity=user.id)

    data = {
      "access_token": access_token,
      "refresh_token": refresh_token
    }

    return data

  @staticmethod
  def register_user(data: dict[str, any]):
    """Register a new user"""
    # Check if user already exists
    existing_user = AuthRepository.get_user_by_email(data["email"])
    if existing_user:
      raise ValidationError("User with this email already exists", 409)
    # Check if password is strong
    if not AuthService.is_password_strong(data["password"]):
      raise ValidationError("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character", 400)
    # Hash password
    data["password"] = AuthService.hash_password(data["password"])
    # Create user
    user = AuthRepository.create_user(data)
    return user

  @staticmethod
  def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    # Generar hash y convertir a string para BD
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

  @staticmethod
  def check_password(password, hashed_password):
    """Verify password using bcrypt"""
    # Convertir hash de string a bytes para verificación
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    
  @staticmethod
  def is_password_strong(password):
    """Check if password is strong"""
    if len(password) < 8:
      return False
    if not any(char.isupper() for char in password):
      return False
    if not any(char.islower() for char in password):
      return False
    if not any(char.isdigit() for char in password):
      return False
    if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?" for char in password):
      return False
    return True

  @staticmethod
  def logout_user():
    """Logout user by blacklisting JWT token"""
    jti = get_jwt()["jti"]
    exp = get_jwt()["exp"]
    
    # Agregar token a blacklist con TTL
    ttl = exp - int(get_jwt()["iat"])
    redis_client.setex(f"blacklist:{jti}", ttl, "revoked")
    
    return {"message": "Token invalidated", "jti": jti}
  
  @staticmethod
  def is_token_blacklisted(jti):
    """Check if token is blacklisted"""
    return redis_client.exists(f"blacklist:{jti}")
from app.repositories.auth_repository import AuthRepository
from app.core.exceptions import ValidationError
import bcrypt

class AuthService:

  @staticmethod
  def login_user(data):
    """Login user"""
    # Check if user exists
    user = AuthRepository.get_user_by_email(data["email"])
    if not user:
      raise ValidationError("User not found", 404)
    # Check if password is correct
    if not AuthService.check_password(data["password"], user.password):
      raise ValidationError("Incorrect password", 401)
    return user

  @staticmethod
  def register_user(data):
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
  def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

  @staticmethod
  def check_password(password, hashed_password):
    """Verify password using bcrypt"""
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
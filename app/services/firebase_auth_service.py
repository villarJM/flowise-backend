import firebase_admin
from firebase_admin import credentials, auth
from flask_jwt_extended import create_access_token, create_refresh_token
from app.repositories.auth_repository import AuthRepository
from app.core.exceptions import ValidationError
import os

class FirebaseAuthService:
    
    @staticmethod
    def initialize_firebase():
        """Inicializar Firebase Admin SDK"""
        if not firebase_admin._apps:
            # Usar service account key file
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH')
            if service_account_path and os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
            else:
                # Usar variables de entorno para credenciales
                firebase_admin.initialize_app()
    
    @staticmethod
    def verify_firebase_token(id_token):
        """Verificar token de Firebase y obtener info del usuario"""
        try:
            FirebaseAuthService.initialize_firebase()
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            raise ValidationError(f"Invalid Firebase token: {str(e)}", 401)
    
    @staticmethod
    def create_or_update_user(firebase_user_info):
        """Crear o actualizar usuario con info de Firebase"""
        email = firebase_user_info.get('email')
        name = firebase_user_info.get('name', '').split(' ')[0] if firebase_user_info.get('name') else ''
        last_name = ' '.join(firebase_user_info.get('name', '').split(' ')[1:]) if firebase_user_info.get('name') else ''
        
        if not email:
            raise ValidationError("Email is required from Firebase token", 400)
        
        # Buscar usuario existente
        user = AuthRepository.get_user_by_email(email)
        
        if not user:
            # Crear nuevo usuario
            user_data = {
                'email': email,
                'name': name,
                'last_name': last_name,
                'password': '',  # Sin contraseña para Firebase Auth
                'role': 'user'
            }
            user = AuthRepository.create_user(user_data)
        else:
            # Actualizar información si es necesario
            if user.name != name or user.last_name != last_name:
                user.name = name
                user.last_name = last_name
                AuthRepository.update_user(user)
        
        # Generar tokens JWT propios
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'last_name': user.last_name,
                'role': user.role
            }
        }
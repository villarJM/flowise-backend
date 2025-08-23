from flask_jwt_extended import JWTManager
from flask import jsonify

from app.core.utils.response_utils import create_response

def configure_jwt(app):
    """Configure JWT with blacklist checking"""
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        # Import aquí para evitar importación circular
        from app.services.auth_service import AuthService
        jti = jwt_payload["jti"]
        return AuthService.is_token_blacklisted(jti)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return create_response("Authorization token is required", 401)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return create_response("Token has expired", 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"Invalid token error: {error}")
        return create_response(f"Invalid token: {str(error)}", 401)

    return jwt
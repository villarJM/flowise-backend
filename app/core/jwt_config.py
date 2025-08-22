from flask_jwt_extended import JWTManager

def configure_jwt(app):
    """Configure JWT with blacklist checking"""
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        # Import aquí para evitar importación circular
        from app.services.auth_service import AuthService
        jti = jwt_payload["jti"]
        return AuthService.is_token_blacklisted(jti)
    
    return jwt
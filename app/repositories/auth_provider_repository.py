from app.models.auth_providers_model import AuthProviderModel, db

class AuthProviderRepository:
    
    @staticmethod
    def create_provider(user_id: int, provider_name: str, provider_uid: str = None) -> AuthProviderModel:
        """Create auth provider for user"""
        provider = AuthProviderModel(
            user_id=user_id,
            provider_name=provider_name,
            provider_uid=provider_uid
        )
        db.session.add(provider)
        db.session.commit()
        return provider
    
    @staticmethod
    def find_by_user_and_provider(user_id: int, provider_name: str) -> AuthProviderModel | None:
        """Find provider by user and provider name"""
        provider = AuthProviderModel.query.filter_by(
            user_id=user_id, 
            provider_name=provider_name
        ).first()
        return provider
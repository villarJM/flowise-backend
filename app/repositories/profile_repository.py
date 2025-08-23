
from app.models.user_model import UserModel, db


class ProfileRepository:
    
    @staticmethod
    def create_user_profile(data: dict[str, any]) -> UserModel:
        """Create a new profile"""
        profileModel = UserModel(**data)
        db.session.add(profileModel)
        db.session.commit()
        return profileModel

    @staticmethod
    def update_user_profile(profile: UserModel, data: dict[str, any]) -> UserModel:
        """Update an existing profile"""
        for key, value in data.items():
            setattr(profile, key, value)
        db.session.commit()
        return profile
    
    @staticmethod
    def find_by_email(email: str) -> UserModel | None:
        """Find a profile by email"""
        profileModel = UserModel.query.filter_by(email=email).first()
        return profileModel

    @staticmethod
    def find_by_id(user_id: int) -> UserModel | None:
        """Find a profile by ID"""
        profileModel = UserModel.query.get(user_id)
        return profileModel
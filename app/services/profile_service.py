
from app.core.exceptions import ValidationError
from app.models.user_model import UserModel
from app.repositories.profile_repository import ProfileRepository


class ProfileService:

    @staticmethod
    def complete_user_profile(user_id: int, data: dict[str, any]) -> UserModel:
        """Complete user profile"""
        if not user_id:
            raise ValidationError("User ID is required", 400)

        found_profile = ProfileRepository.find_by_id(user_id)
        if not found_profile:
            raise ValidationError("Profile not found", 404)

        profileModel = ProfileRepository.update_user_profile(found_profile, data)
        return profileModel

    @staticmethod
    def update_user_profile(user_id: int, data: dict[str, any]) -> UserModel:
        """Update an existing profile"""
        if not user_id:
            raise ValidationError("User ID is required", 400)
        
        found_profile = ProfileRepository.find_by_id(user_id)
        if not found_profile:
            raise ValidationError("Profile not found", 404)

        profileModel = ProfileRepository.update_user_profile(found_profile, data)
        return profileModel
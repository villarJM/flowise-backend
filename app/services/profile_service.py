
from app.core.exceptions import ValidationError
from app.models.user_model import UserModel
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile_register_schema import ProfileRegisterSchema


class ProfileService:

    @staticmethod
    def create_user_profile(user_id: int, data: dict[str, any]):
        """Register a new profile"""
        if not user_id:
            raise ValidationError("User ID is required", 400)

        found_profile = ProfileRepository.find_by_id(user_id)
        if found_profile:
            raise ValidationError("Profile with this ID already exists", 409)

        profile = ProfileRepository.create_user_profile(data)
        return profile

    @staticmethod
    def update_user_profile(user_id: int, data: dict[str, any]):
        """Update an existing profile"""
        if not user_id:
            raise ValidationError("User ID is required", 400)
        
        found_profile = ProfileRepository.find_by_id(user_id)
        if not found_profile:
            raise ValidationError("Profile not found", 404)

        result_profile = ProfileRepository.update_user_profile(found_profile, data)
        return result_profile
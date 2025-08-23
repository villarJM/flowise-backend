from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError as MarshmallowValidationError
from app.services.profile_service import ProfileService
from app.schemas.user_update_schema import UserUpdateSchema
from app.core.utils.response_utils import create_response
from app.core.exceptions import ValidationError

bp = Blueprint("profile", __name__, url_prefix='/profile')

# Create user profile
@bp.route("/create", methods=["POST"])
@jwt_required()
def create_user_profile():
    if not request.is_json:
        return create_response("Content-Type must be application/json", 415)

    if not request.json:
        return create_response("Request body is empty", 400)

    user_id = get_jwt_identity()
    user_schema = UserUpdateSchema()

    try:
        data = user_schema.load(request.json)
    except MarshmallowValidationError as err:
        return create_response("Fields Invalid", 400, err.messages)

    try:
        new_profile = ProfileService.create_user_profile(user_id, data)
        return create_response("Profile created successfully", 201, user_schema.dump(new_profile))
    except ValidationError as err:
        return create_response(str(err), err.code)
    except Exception as err:
        return create_response("Profile creation failed", 500, str(err))

# Update user profile
@bp.route("/update", methods=["PUT"])
@jwt_required()
def update_user_profile():
    if not request.is_json:
        return create_response("Content-Type must be application/json", 415)

    if not request.json:
        return create_response("Request body is empty", 400)

    user_id = get_jwt_identity()
    user_schema = UserUpdateSchema()

    try:
        data = user_schema.load(request.json)
    except MarshmallowValidationError as err:
        return create_response("Fields Invalid", 400, err.messages)

    try:
        updated_user = ProfileService.update_user_profile(user_id, data)
        return create_response("Profile updated successfully", 200, user_schema.dump(updated_user))
    except ValidationError as err:
        return create_response(str(err), err.code)
    except Exception as err:
        return create_response("Profile update failed", 500, str(err))
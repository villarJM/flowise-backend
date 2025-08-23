from app.models.user_model import UserModel, db

class AuthRepository:
  
    @staticmethod
    def create_user(data: dict[str, any]) -> UserModel:
        userModel = UserModel(**data)
        db.session.add(userModel)
        db.session.commit()
        return userModel

    @staticmethod
    def get_user_by_email(email: str) -> UserModel | None:
        userModel = UserModel.query.filter_by(email=email).first()
        return userModel
    
    @staticmethod
    def update_user(user: UserModel, data: dict[str, any]) -> UserModel:
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return user
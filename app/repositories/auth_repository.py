from app.models.user_model import UserModel, db

class AuthRepository:
  
  @staticmethod
  def create_user(data):
    user = UserModel(**data)
    db.session.add(user)
    db.session.commit()
    return user

  @staticmethod
  def get_user_by_email(email):
    user = UserModel.query.filter_by(email=email).first()
    return user
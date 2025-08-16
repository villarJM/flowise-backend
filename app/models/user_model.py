from app import db

class UserModel(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.String, primary_key=True)
  name = db.Column(db.String(36), nullable=False)
  last_name = db.Column(db.String(100))
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  role = db.Column(db.String(50))
  company = db.Column(db.String(100))
  created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

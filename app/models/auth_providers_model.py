from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AuthProviderModel(db.Model):
  __tablename__ = 'auth_providers'
  id = db.Column(db.String, primary_key=True)
  user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
  provider_name = db.Column(db.String(50))
  provider_uid = db.Column(db.String(255))
  created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
from app import db

class ProjectModel(db.Model):
  __tablename__ = 'projects'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  project_code = db.Column(db.String(50), unique=True)
  name = db.Column(db.String(100))
  description = db.Column(db.Text)
  status = db.Column(db.String(50))
  start_date = db.Column(db.Date)
  end_date = db.Column(db.Date)
  created_by = db.Column(db.String(36))
  created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
  updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

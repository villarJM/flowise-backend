from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserProjectModel(db.Model):
    __tablename__ = 'user_projects'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.String, db.ForeignKey('projects.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    __table_args__ = (db.UniqueConstraint('user_id', 'project_id', name='_user_project_uc'),)

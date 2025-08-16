from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProjectCommentModel(db.Model):
    __tablename__ = 'project_comments'
    id = db.Column(db.String, primary_key=True)
    project_id = db.Column(db.String, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    comment_text = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
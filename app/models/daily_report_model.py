from app import db

class DailyReportModel(db.Model):
    __tablename__ = 'daily_reports'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.String, db.ForeignKey('projects.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    total_hours = db.Column(db.Float)
    type = db.Column(db.String(10))  # CP o CU
    generated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    completed = db.Column(db.Boolean, default=False)
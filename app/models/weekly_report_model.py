from app import db

class WeeklyReport(db.Model):
    __tablename__ = 'weekly_reports'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    week_start_date = db.Column(db.Date, nullable=False)
    week_end_date = db.Column(db.Date, nullable=False)
    total_hours = db.Column(db.Float)
    total_projects = db.Column(db.Integer)
    generated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

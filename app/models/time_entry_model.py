from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
 
class TimeEntryModel(db.Model):
    __tablename__ = 'time_entries'
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.String, db.ForeignKey('projects.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # CP o CU
    status = db.Column(db.String(20), default='running')  # running, paused, completed, interrupted
    planned_hours = db.Column(db.Float)
    actual_hours = db.Column(db.Float)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    interrupted_by = db.Column(db.String, db.ForeignKey('time_entries.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

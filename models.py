from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class CalendarModel(db.Model):
    __tablename__ = "events"

    event_id = db.Column(db.Integer, primary_key=True)
    event_time = db.Column(db.String())
    description = db.Column(db.String())

    def __init__(self, id_, time_, description):
        self.event_id = id_
        self.event_time = time_
        self.description = description

    def get_event(self):
        return {'description': self.description, 'event_id': self.event_id, 'event_time': self.event_time}
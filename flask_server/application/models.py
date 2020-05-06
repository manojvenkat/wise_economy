from application import db

class TrackingRecord(db.Model):
    __tablename__ = 'tracking_records'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True)
    channel = db.Column(db.String(256), index=True)
    country = db.Column(db.String(256), index=True)
    os = db.Column(db.String(256), index=True)
    impressions = db.Column(db.Integer)
    clicks = db.Column(db.Integer)
    installs = db.Column(db.Integer)
    spend = db.Column(db.Integer)
    revenue = db.Column(db.Float)

    def __repr__(self):
        return self.channel + " " + self.os + " " + self.country


def name_to_column_dict():
    return {column.name: column for column in TrackingRecord.__table__.columns.values()}
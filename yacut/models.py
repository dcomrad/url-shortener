from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.Text, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self, host) -> dict:
        return dict(
            url=self.original,
            short_link=host + self.short,
        )

    def from_dict(self, data):
        setattr(self, 'original', data.get('url', ''))
        setattr(self, 'short', data.get('custom_id', ''))

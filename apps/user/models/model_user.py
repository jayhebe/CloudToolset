from datetime import datetime

from exts import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    reg_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __str__(self):
        return self.email

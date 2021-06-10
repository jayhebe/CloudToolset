from exts import db


class Environment(db.Model):
    env_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    env_name = db.Column(db.String(50), nullable=False)
    env_display_name = db.Column(db.String(50), nullable=False)

    def __str__(self):
        return self.env_name

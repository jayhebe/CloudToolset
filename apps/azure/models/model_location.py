from exts import db


class Location(db.Model):
    loc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    loc_name = db.Column(db.String(255), nullable=False)
    loc_display_name = db.Column(db.String(255), nullable=False)
    loc_full_name = db.Column(db.String(255), nullable=False)
    env_id = db.Column(db.Integer, db.ForeignKey("environment.env_id"))
    environment = db.relationship("Environment", backref=db.backref("location"))

    def __str__(self):
        return self.loc_name

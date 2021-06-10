from exts import db


class Subscription(db.Model):
    sub_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subscription_id = db.Column(db.String(36), nullable=False)
    subscription_name = db.Column(db.String(255), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=False)
    application_id = db.Column(db.String(36), nullable=False)
    application_key = db.Column(db.String(34), nullable=False)

    env_id = db.Column(db.Integer, db.ForeignKey("environment.env_id"))
    environment = db.relationship("Environment", backref=db.backref("subscription"))

    loc_id = db.Column(db.Integer, db.ForeignKey("location.loc_id"))
    location = db.relationship("Location", backref=db.backref("subscription"))

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User", backref=db.backref("subscription"))

    def __str__(self):
        return self.subscription_name

from exts import db


class Keyvault(db.Model):
    keyvault_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyvault_name = db.Column(db.String(255), nullable=False)
    tenant_id = db.Column(db.String(36), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User", backref=db.backref("keyvault"))

    env_id = db.Column(db.Integer, db.ForeignKey("environment.env_id"))
    environment = db.relationship("Environment", backref=db.backref("keyvault"))

    def __str__(self):
        return self.keyvault_name

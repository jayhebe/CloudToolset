from exts import db


class KeyvaultSecret(db.Model):
    secret_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    secret_name = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    expires_on = db.Column(db.DateTime)

    keyvault_id = db.Column(db.Integer, db.ForeignKey("keyvault.keyvault_id"))
    keyvault = db.relationship("Keyvault", backref=db.backref("keyvault_secret"))

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User", backref=db.backref("keyvault_secret"))

    def __str__(self):
        return self.secret_name

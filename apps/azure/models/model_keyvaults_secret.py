from exts import db


class KeyvaultsSecret(db.Model):
    secret_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    secret_name = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    updated_on = db.Column(db.DateTime, nullable=False)
    expires_on = db.Column(db.DateTime, nullable=False)

    keyvaults_id = db.Column(db.Integer, db.ForeignKey("keyvaults.keyvaults_id"))
    keyvaults = db.relationship("Keyvaults", backref=db.backref("keyvaults_secret"))

    def __str__(self):
        return self.secret_name

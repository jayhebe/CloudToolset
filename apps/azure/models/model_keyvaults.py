from exts import db


class Keyvaults(db.Model):
    keyvaults_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyvaults_name = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    user = db.relationship("User", backref=db.backref("keyvaults"))

    def __str__(self):
        return self.keyvaults_name

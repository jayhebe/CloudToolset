from flask import Blueprint, request, render_template, jsonify
from werkzeug.security import generate_password_hash

from apps.user.model_user import User
from exts import db

bp_user = Blueprint("user", __name__, url_prefix="/user")


@bp_user.route("/register", methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User()
        user.email = email
        user.password = generate_password_hash(password)

        db.session.add(user)
        db.session.commit()

        return render_template("index/index.html", msg="注册成功")

    return render_template("user/register.html")


@bp_user.route("/login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        pass

    return render_template("user/login.html")


@bp_user.route("/check_email")
def user_check_email():
    email = request.args.get("email")
    user = User.query.filter(User.email == email).first()
    if user:
        return jsonify(exists=1)
    else:
        return jsonify(exists=0)

import functools

from flask import Blueprint, request, render_template, jsonify, session, g, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from apps.user.models.model_user import User
from exts import db

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_auth.route("/register", methods=["GET", "POST"])
def auth_register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User()
        user.email = email
        user.password = generate_password_hash(password)

        db.session.add(user)
        db.session.commit()

        return render_template("index/index.html", msg="注册成功")

    return render_template("auth/register.html")


@bp_auth.route("/login", methods=["GET", "POST"])
def auth_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter(User.email == email).first()
        if user and check_password_hash(user.password, password):
            session.clear()
            session["user_id"] = user.user_id

            return redirect(url_for("index.index"))
        else:
            return render_template("auth/login.html", msg="用户名或密码错误")

    return render_template("auth/login.html")


@bp_auth.route("/logout")
def auth_logout():
    session.clear()

    return redirect(url_for("index.index"))


@bp_auth.route("/check_email")
def auth_check_email():
    email = request.args.get("email")
    user = User.query.filter(User.email == email).first()
    if user:
        return jsonify(exists=1)
    else:
        return jsonify(exists=0)


@bp_auth.before_app_request
def auth_load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.user_id == user_id).first()


def auth_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.auth_login"))

        return view(**kwargs)

    return wrapped_view

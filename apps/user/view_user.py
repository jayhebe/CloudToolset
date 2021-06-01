from flask import Blueprint, request, render_template

bp_user = Blueprint("user", __name__, url_prefix="/user")


@bp_user.route("/register")
def user_register():
    if request.method == "POST":
        pass

    return render_template("user/register.html")


@bp_user.route("/login")
def user_login():
    if request.method == "POST":
        pass

    return render_template("user/login.html")

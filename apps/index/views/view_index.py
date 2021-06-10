from flask import Blueprint, render_template

bp_index = Blueprint("index", __name__)


@bp_index.route("/")
@bp_index.route("/index")
def index():
    return render_template("index/index.html")

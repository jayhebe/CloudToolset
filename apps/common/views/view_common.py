from flask import Blueprint, request, render_template

from apps.auth.views.view_auth import auth_login_required

import string
import random
import requests
from bs4 import BeautifulSoup

bp_common = Blueprint("common", __name__, url_prefix="/common")


@bp_common.route("/password", methods=["GET", "POST"])
@auth_login_required
def common_generate_password():
    if request.method == "POST":
        length = request.form.get("password_length")
        password = generate_password(int(length))

        return render_template("common/password.html", password=password)

    return render_template("common/password.html")


@bp_common.route("/ipaddress")
@auth_login_required
def common_get_my_ip():
    ip_address = get_my_ip()

    return render_template("common/ip.html", ip_address=ip_address)


def generate_password(length):
    password = ""
    special_chars = "^*()-=+"
    for _ in range(length):
        password += random.choice(string.digits + string.ascii_letters + special_chars)

    return password


def get_my_ip():
    ip_url = "http://www.net.cn/static/customercare/yourip.asp"
    ip_res = requests.get(ip_url)
    ip_bs = BeautifulSoup(ip_res.text, "html.parser")
    ip_address = ip_bs.find("h2").text

    return ip_address

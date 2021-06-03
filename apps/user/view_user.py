from flask import Blueprint, request, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from apps.user.model_user import User
from exts import db

bp_user = Blueprint("user", __name__, url_prefix="/user")

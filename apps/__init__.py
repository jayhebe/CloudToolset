from flask import Flask

from apps.auth.view_auth import bp_auth
from apps.azure.view_keyvaults import bp_azure
from apps.index.view_index import bp_index
from apps.user.view_user import bp_user
from exts import db
from settings import settings


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(settings.DevelopmentConfig)

    app.register_blueprint(bp_index)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_azure)

    db.init_app(app)

    return app

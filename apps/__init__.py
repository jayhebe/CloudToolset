from flask import Flask

from apps.auth.views.view_auth import bp_auth
from apps.azure.views.view_keyvault import bp_keyvaults
from apps.azure.views.view_subscription import bp_subscription
from apps.common.views.view_common import bp_common
from apps.index.views.view_index import bp_index
from apps.tools.view_tools import bp_tools
from apps.user.views.view_user import bp_user
from exts import db
from settings import settings


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(settings.DevelopmentConfig)

    app.register_blueprint(bp_index)
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_keyvaults)
    app.register_blueprint(bp_subscription)
    app.register_blueprint(bp_common)
    app.register_blueprint(bp_tools)

    db.init_app(app)

    return app

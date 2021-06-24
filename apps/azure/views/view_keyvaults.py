from flask import Blueprint, request, render_template, current_app, g

from apps.auth.views.view_auth import auth_login_required
from apps.azure.models.model_environment import Environment
from apps.azure.models.model_subscription import Subscription
from apps.azure.utils.azure_credential import get_credential
from apps.azure.utils.azure_keyvaults import get_kv_secret

bp_keyvaults = Blueprint("keyvaults", __name__, url_prefix="/azure")


@bp_keyvaults.route("/secret_search", methods=["GET", "POST"])
@auth_login_required
def azure_get_secret():
    envs = Environment.query.all()
    tenants = Subscription.query.filter(Subscription.env_id == 1, Subscription.user_id == g.user.user_id).all()

    if request.method == "POST":
        environment = request.form.get("environment")
        tenant_id = request.form.get("tenant_id")
        client_id = request.form.get("client_id")
        client_secret = request.form.get("client_secret")
        keyvaults_name = request.form.get("keyvaults_name")
        secret_name = request.form.get("secret_name")

        try:
            credential = get_credential(
                client_id=client_id,
                client_secret=client_secret,
                tenant_id=tenant_id,
                env=environment
            )

            secret_value = get_kv_secret(
                keyvaults_name=keyvaults_name,
                secret_name=secret_name,
                credential=credential,
                env=environment
            )
        except Exception as e:
            secret_value = "One or more of the following values is not correct."
            current_app.logger.error(e)

        return render_template("azure/secret_search.html", secret_value=secret_value, envs=envs, tenants=tenants)

    return render_template("azure/secret_search.html", envs=envs, tenants=tenants)


@bp_keyvaults.route("/secret_mgmt", methods=["GET", "POST"])
@auth_login_required
def azure_get_all_secrets():
    pass

from flask import Blueprint, request, render_template, current_app

from apps.auth.views.view_auth import auth_login_required
from apps.azure.models.model_environment import Environment
from apps.azure.utils.azure_credential import get_credential
from apps.azure.utils.azure_keyvaults import get_kv_secret

bp_keyvaults = Blueprint("keyvaults", __name__, url_prefix="/azure")


@bp_keyvaults.route("/keyvaults", methods=["GET", "POST"])
@auth_login_required
def azure_keyvaults():
    envs = Environment.query.all()

    if request.method == "POST":
        tenant_id = current_app.config["TENANT_ID"]
        environment = request.form.get("environment")
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

        return render_template("azure/keyvaults.html", secret_value=secret_value, envs=envs)

    return render_template("azure/keyvaults.html", envs=envs)

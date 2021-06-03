from flask import Blueprint, request, render_template, current_app

from apps.auth.view_auth import auth_login_required
from apps.azure.utils.azure_credential import get_credential
from apps.azure.utils.azure_keyvaults import get_kv_secret

bp_azure = Blueprint("azure", __name__, url_prefix="/azure")


@bp_azure.route("/keyvaults", methods=["GET", "POST"])
@auth_login_required
def azure_keyvaults():
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
            print(e)

        return render_template("azure/keyvaults.html", secret_value=secret_value)

    return render_template("azure/keyvaults.html")

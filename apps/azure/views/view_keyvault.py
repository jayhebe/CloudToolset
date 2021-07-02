from flask import Blueprint, request, render_template, current_app, g, redirect, url_for

from apps.auth.views.view_auth import auth_login_required
from apps.azure.models.model_environment import Environment
from apps.azure.models.model_keyvault import Keyvault
from apps.azure.models.model_keyvault_secret import KeyvaultSecret
from apps.azure.models.model_subscription import Subscription
from apps.azure.utils.azure_credential import get_credential
from apps.azure.utils.azure_keyvault import get_kv_secret
from exts import db

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
        keyvault_name = request.form.get("keyvault_name")
        secret_name = request.form.get("secret_name")

        try:
            credential = get_credential(
                client_id=client_id,
                client_secret=client_secret,
                tenant_id=tenant_id,
                env=environment
            )

            secret_value = get_kv_secret(
                keyvault_name=keyvault_name,
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
    secrets = KeyvaultSecret.query.filter(KeyvaultSecret.user_id == g.user.user_id).all()

    return render_template("azure/secret_mgmt.html", secrets=secrets)


@bp_keyvaults.route("/keyvault_add", methods=["GET", "POST"])
@auth_login_required
def azure_keyvault_add():
    envs = Environment.query.all()
    tenants = Subscription.query.filter(Subscription.env_id == 1, Subscription.user_id == g.user.user_id).all()

    if request.method == "POST":
        env_id = request.form.get("environment")
        tenant_id = request.form.get("tenant_id")
        keyvault_name = request.form.get("keyvault_name")

        keyvault = Keyvault()
        keyvault.keyvault_name = keyvault_name
        keyvault.env_id = env_id
        keyvault.tenant_id = tenant_id
        keyvault.user_id = g.user.user_id

        db.session.add(keyvault)
        db.session.commit()

        subscription = Subscription.query.filter(
            Subscription.env_id == env_id,
            Subscription.tenant_id == tenant_id,
            Subscription.user_id == g.user.user_id
        ).first()

        try:
            credential = get_credential(
                client_id=subscription.application_id,
                client_secret=subscription.application_key,
                tenant_id=tenant_id,
                env=subscription.environment.env_name
            )

            secrets = get_kv_secret(
                keyvault_name=keyvault_name,
                credential=credential,
                env=subscription.environment.env_name
            )
        except Exception as e:
            secrets = None
            current_app.logger.error(e)

        if secrets:
            keyvault = Keyvault.query.filter(
                Keyvault.keyvault_name == keyvault_name,
                Keyvault.env_id == env_id,
                Keyvault.tenant_id == tenant_id,
                Keyvault.user_id == g.user.user_id
            ).first()

            for secret in secrets:
                keyvault_secret = KeyvaultSecret()
                keyvault_secret.secret_name = secret.name
                keyvault_secret.created_on = secret.created_on
                keyvault_secret.updated_on = secret.updated_on
                keyvault_secret.expires_on = secret.expires_on
                keyvault_secret.user_id = g.user.user_id

                keyvault_secret.keyvault_id = keyvault.keyvault_id

                db.session.add(keyvault_secret)
                db.session.commit()

        return redirect(url_for("keyvaults.azure_get_all_keyvaults"))

    return render_template("azure/keyvault_add.html", envs=envs, tenants=tenants)


@bp_keyvaults.route("/keyvault_mgmt")
@auth_login_required
def azure_get_all_keyvaults():
    keyvaults = Keyvault.query.filter(Keyvault.user_id == g.user.user_id).all()

    return render_template("azure/keyvault_mgmt.html", keyvaults=keyvaults)

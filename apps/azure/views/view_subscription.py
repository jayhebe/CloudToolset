from flask import Blueprint, request, render_template, g, flash, url_for
from werkzeug.utils import redirect

from apps.auth.views.view_auth import auth_login_required
from apps.azure.models.model_environment import Environment
from apps.azure.models.model_location import Location
from apps.azure.models.model_subscription import Subscription
from exts import db

bp_subscription = Blueprint("subscription", __name__, url_prefix="/azure")


@bp_subscription.route("/subscription")
@auth_login_required
def azure_subscription():
    subs = Subscription.query.filter(Subscription.user_id == g.user.user_id).all()
    return render_template("/azure/subscription.html", subs=subs)


@bp_subscription.route("/subscription_add", methods=["GET", "POST"])
@auth_login_required
def azure_subscription_add():
    envs = Environment.query.all()
    locations = Location.query.filter(Location.env_id == 1).order_by(Location.loc_full_name).all()

    if request.method == "POST":
        env_id = request.form.get("environment")
        tenant_id = request.form.get("tenant_id")
        subscription_id = request.form.get("subscription_id")
        subscription_name = request.form.get("subscription_name")
        loc_id = request.form.get("location")
        user_id = g.user.user_id
        application_id = request.form.get("application_id")
        application_key = request.form.get("application_key")

        subscription = Subscription()
        subscription.subscription_id = subscription_id
        subscription.subscription_name = subscription_name
        subscription.env_id = env_id
        subscription.loc_id = loc_id
        subscription.user_id = user_id
        subscription.tenant_id = tenant_id
        subscription.application_id = application_id
        subscription.application_key = application_key

        db.session.add(subscription)
        db.session.commit()

        flash("Saved successfully")
        return redirect(url_for("subscription.azure_subscription"))

    return render_template("azure/subscription_add.html", envs=envs, locations=locations)

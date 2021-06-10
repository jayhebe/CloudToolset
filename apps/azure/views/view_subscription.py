from flask import Blueprint, request, render_template, jsonify, g, flash

from apps.auth.views.view_auth import auth_login_required
from apps.azure.models.model_environment import Environment
from apps.azure.models.model_location import Location
from apps.azure.models.model_subscription import Subscription
from exts import db

bp_subscription = Blueprint("subscription", __name__, url_prefix="/azure")


@bp_subscription.route("/subscription", methods=["GET", "POST"])
@auth_login_required
def azure_subscription():
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
        return render_template("azure/subscription.html", envs=envs, locations=locations)

    return render_template("azure/subscription.html", envs=envs, locations=locations)


@bp_subscription.route("/get_locations")
def azure_get_locations():
    loc_full_names = []
    env_id = request.args.get("env_id")
    locations = Location.query.filter(Location.env_id == env_id).order_by(Location.loc_full_name).all()
    for location in locations:
        loc_full_names.append({"loc_id": location.loc_id, "loc_full_name": location.loc_full_name})

    return jsonify(loc_full_names)

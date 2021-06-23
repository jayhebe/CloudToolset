from flask import Blueprint, request, jsonify, g

from apps.auth.views.view_auth import auth_login_required
from apps.azure.models.model_location import Location
from apps.azure.models.model_subscription import Subscription

bp_tools = Blueprint("tools", __name__, url_prefix="/tools")


@bp_tools.route("/get_locations")
def azure_get_locations():
    loc_full_names = []
    env_id = request.args.get("env_id")
    locations = Location.query.filter(Location.env_id == env_id).order_by(Location.loc_full_name).all()
    for location in locations:
        loc_full_names.append({"loc_id": location.loc_id, "loc_full_name": location.loc_full_name})

    return jsonify(loc_full_names)


@bp_tools.route("/get_tenant_id")
@auth_login_required
def azure_get_tenant_id():
    tenant_ids = []
    env_id = request.args.get("env_id")
    tenants = Subscription.query.filter(Subscription.env_id == env_id, Subscription.user_id == g.user.user_id).all()
    if tenants:
        for tenant in tenants:
            tenant_ids.append({"tenant_id": tenant.tenant_id})
    else:
        tenant_ids.append({"tenant_id": "You do not have any tenant ID in this environment, please add one."})

    return jsonify(tenant_ids)

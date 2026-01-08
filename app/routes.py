from flask import Blueprint, render_template, request, abort, jsonify
from app import limiter
from .data import get_all_apis, get_api_by_id
from .api_helpers import (
    handle_cat_facts_api,
    handle_dog_ceo_api,
    handle_jokeapi,
    handle_default_api,
    handle_dog_api,
    handle_advice_slip_api,
    handle_kanye_rest_api,
    handle_dad_jokes_api,
)

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    apis = get_all_apis()
    return render_template('index.html', apis=apis)

@bp.route('/api/<int:api_id>', methods=['GET', 'POST'])
@limiter.limit("30 per minute", methods=['POST'])  # Only rate limit POST requests
def api_detail(api_id):
    api = get_api_by_id(api_id)
    if not api:
        abort(404)

    result = None
    result_type = None

    # Only process POST requests (API calls)
    if request.method == 'POST':

        # Build parameters from form data
        params = {}
        if api.get("parameters"):
            for param in api["parameters"]:
                value = request.form.get(param["name"])
                if value:
                    # Input validation: prevent DoS attacks with very long parameters
                    if len(str(value)) > 500:
                        return render_template(
                            'api_detail.html',
                            api=api,
                            result="Parameter too long (max 500 characters)",
                            result_type="error"
                        )
                    params[param["name"]] = value

        # Dispatch to helper based on API name
        api_name = api.get('name', '').lower()
        try:
            if api_name == "cat facts":
                result, result_type = handle_cat_facts_api(api)
            elif api_name == "dog ceo":
                result, result_type = handle_dog_ceo_api(api)
            elif api_name == "jokeapi":
                result, result_type = handle_jokeapi(api, params)
            elif api_name == "dogapi":
                result, result_type = handle_dog_api(api, params)
            elif api_name == "advice slip":
                result, result_type = handle_advice_slip_api(api)
            elif api_name == "kanye rest":
                result, result_type = handle_kanye_rest_api(api)
            elif api_name == "dad jokes":
                result, result_type = handle_dad_jokes_api(api)
            else:
                result, result_type = handle_default_api(api, params)
        except Exception as e:
            # Don't expose internal errors to users
            result = "An error occurred while calling the API. Please try again."
            result_type = "error"

    return render_template('api_detail.html', api=api, result=result, result_type=result_type)

from flask import Blueprint, render_template, request, abort
from app import limiter
from .data import get_all_apis, get_api_by_id
from . import api_handlers

bp = Blueprint('main', __name__)


def get_handler(api):
    """
    Get the appropriate handler for an API.

    If has_handler is True, looks for a handler function named:
    handle_{api_name.lower().replace(' ', '_')}_api

    Falls back to handle_default_api if no custom handler is found.
    """
    if not api.get('has_handler'):
        return api_handlers.handle_default_api

    # Convert API name to handler function name
    # "Dog CEO" -> "handle_dog_ceo_api"
    # "JokeAPI" -> "handle_jokeapi_api"
    handler_name = f"handle_{api.get('name', '').lower().replace(' ', '_')}_api"
    handler = getattr(api_handlers, handler_name, None)

    if handler:
        return handler
    else:
        # Handler not found, fall back to default
        return api_handlers.handle_default_api


@bp.route('/')
def index():
    apis = get_all_apis()
    return render_template('index.html', apis=apis)

@bp.route('/api/<int:api_id>', methods=['GET', 'POST'])
@limiter.limit("10 per minute", methods=['POST'])  # Only rate limit POST requests
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

        # Get handler and call it
        try:
            handler = get_handler(api)
            result, result_type = handler(api, params)
        except Exception:
            # Don't expose internal errors to users
            result = "An error occurred while calling the API. Please try again."
            result_type = "error"

    return render_template('api_detail.html', api=api, result=result, result_type=result_type)

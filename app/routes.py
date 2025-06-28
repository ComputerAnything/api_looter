from flask import Blueprint, render_template, request
from .models import APIModel
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
    apis = APIModel.query.order_by(APIModel.name.asc()).all()
    return render_template('index.html', apis=apis)

@bp.route('/api/<int:api_id>', methods=['GET', 'POST'])
def api_detail(api_id):
    api = APIModel.query.get_or_404(api_id)
    result = None
    result_type = None
    if request.method == 'POST':
        params = {param["name"]: request.form.get(param["name"]) for param in api.parameters} if api.parameters else None

        # Dispatch to helper based on API name
        if api.name.lower() == "cat facts":
            result, result_type = handle_cat_facts_api(api)
        elif api.name.lower() == "dog ceo":
            result, result_type = handle_dog_ceo_api(api)
        elif api.name.lower() == "jokeapi":
            result, result_type = handle_jokeapi(api, params)
        elif api.name.lower() == "dogapi":
            result, result_type = handle_dog_api(api, params)
        elif api.name.lower() == "advice slip":
            result, result_type = handle_advice_slip_api(api)
        elif api.name.lower() == "kanye rest":
            result, result_type = handle_kanye_rest_api(api)
        elif api.name.lower() == "dad jokes":
            result, result_type = handle_dad_jokes_api(api)
        else:
            result, result_type = handle_default_api(api, params)
    return render_template('api_detail.html', api=api, result=result, result_type=result_type)

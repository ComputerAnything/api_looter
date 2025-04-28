from flask import Blueprint, render_template, request
from .models import APIModel
import requests

bp = Blueprint('main', __name__)

# Cat Facts API Helper
def handle_cat_facts_api(api, params=None):
    response = requests.get(api.endpoint, headers={"Accept": "application/json"})
    return parse_response(response)

# Dog CEO API Helper
def handle_dog_ceo_api(api, params=None):
    response = requests.get(api.endpoint, headers={"Accept": "application/json"})
    return parse_response(response)

# JokeAPI Helper
def handle_jokeapi(api, params=None):
    response = requests.get(api.endpoint, params=params, headers={"Accept": "application/json"})
    return parse_jokeapi_response(response)

def parse_jokeapi_response(response):
    try:
        data = response.json()
        joke = {
            "category": data.get("category"),
            "setup": data.get("setup") or data.get("joke"),
            "delivery": data.get("delivery", "")
        }
        return joke, "joke"
    except Exception:
        return response.text, "text"

# Default API Helper
def handle_default_api(api, params=None):
    response = requests.get(api.endpoint, params=params, headers={"Accept": "application/json"})
    return parse_response(response)

def parse_response(response):
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            data = response.json()
            # Dog CEO special case (if not routed separately)
            if isinstance(data, dict) and "message" in data and isinstance(data["message"], str) and data["message"].startswith("http"):
                return data["message"], "image"
            return data, "json"
        except Exception:
            return response.text, "text"
    elif "image" in content_type:
        return response.url, "image"
    else:
        return response.text, "text"

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
        else:
            result, result_type = handle_default_api(api, params)
    return render_template('api_detail.html', api=api, result=result, result_type=result_type)

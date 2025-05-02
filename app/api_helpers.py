import requests

def parse_response(response):
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            data = response.json()
            if isinstance(data, dict) and "message" in data and isinstance(data["message"], str) and data["message"].startswith("http"):
                return data["message"], "image"
            return data, "json"
        except Exception:
            return response.text, "text"
    elif "image" in content_type:
        return response.url, "image"
    else:
        return response.text, "text"

def handle_cat_facts_api(api, params=None):
    response = requests.get(api.endpoint, headers={"Accept": "application/json"})
    return parse_response(response)

def handle_dog_ceo_api(api, params=None):
    response = requests.get(api.endpoint, headers={"Accept": "application/json"})
    return parse_response(response)

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

def handle_default_api(api, params=None):
    response = requests.get(api.endpoint, params=params, headers={"Accept": "application/json"})
    return parse_response(response)

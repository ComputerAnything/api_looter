import json
import requests


def parse_response(response):
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            data = response.json()
            if isinstance(data, dict) and "message" in data and isinstance(data["message"], str) and data["message"].startswith("http"):
                return data["message"], "image"
            # Serialize JSON data to ensure proper escaping
            return json.dumps(data, indent=2), "json"
        except Exception:
            return response.text, "text"
    elif "image" in content_type:
        return response.url, "image"
    else:
        return response.text, "text"

# Cat Facts API
def handle_cat_facts_api(api, params=None):
    response = requests.get(api.endpoint, headers={"Accept": "application/json"})
    try:
        data = response.json()
        # Extract the "fact" field from the response
        fact = data["fact"]
        return fact, "text"  # Return as plain text
    except (KeyError, ValueError):
        return "Failed to parse Cat Facts API response.", "text"

# Dog CEO API
def handle_dog_ceo_api(api, params=None):
    response = requests.get(api.endpoint, headers={"Accept": "application/json"})
    return parse_response(response)

# DogAPI
def handle_dog_api(api, params=None):
    response = requests.get(api.endpoint, headers={"Accept": "application/json"})
    try:
        data = response.json()
        # Extract the "body" field from the first item in "data"
        fact = data["data"][0]["attributes"]["body"]
        return fact, "text"  # Return as plain text
    except (KeyError, IndexError, ValueError):
        return "Failed to parse DogAPI response.", "text"

# JokeAPI
def handle_jokeapi(api, params=None):
    # Extract the category from params and construct the endpoint
    params = params or {}  # Ensure params is a dictionary
    category = params.pop("category", "Any")  # Default to "Any" if no category is selected
    endpoint = f"https://v2.jokeapi.dev/joke/{category}"

    # Make the API request with the updated endpoint and remaining params
    response = requests.get(endpoint, params=params, headers={"Accept": "application/json"})
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

# Advice Slip API
def handle_advice_slip_api(api, params=None):
    response = requests.get(api.endpoint, headers={"Accept": "application/json"})
    try:
        data = response.json()
        # Extract the "advice" field from the "slip" object
        advice = data["slip"]["advice"]
        return advice, "text"  # Return as plain text
    except (KeyError, ValueError):
        return "Failed to parse Advice Slip API response.", "text"

# Dad Jokes API
def handle_dad_jokes_api(api, params=None):
    response = requests.get(api.endpoint, headers={"Accept": "application/json"})
    try:
        data = response.json()
        # Extract the "joke" field from the response
        joke = data["joke"]
        return joke, "text"  # Return as plain text
    except (KeyError, ValueError):
        return "Failed to parse Dad Jokes API response.", "text"

def handle_kanye_rest_api(api, params=None):
    response = requests.get(api.endpoint, headers={"Accept": "application/json"})
    try:
        data = response.json()
        # Extract the "quote" field from the response
        quote = data["quote"]
        return quote, "text"  # Return as plain text
    except (KeyError, ValueError):
        return "Failed to parse Kanye Rest API response.", "text"

def handle_default_api(api, params=None):
    response = requests.get(api.endpoint, params=params, headers={"Accept": "application/json"})
    return parse_response(response)

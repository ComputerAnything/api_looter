"""
Static API data structure for api_looter.
No database needed - all API information stored here.
"""

APIS = [
    {
        "id": 1,
        "name": "Dog CEO",
        "description": "Random pictures of dogs.",
        "endpoint": "https://dog.ceo/api/breeds/image/random",
        "parameters": [],
        "why_use": "Great for placeholder images, testing image handling, or building pet-related apps.",
        "how_use": "Perfect for learning HTTP requests - no API key needed, returns JSON with image URL. Ideal for beginners practicing API calls.",
        "category": "Images",
        "has_handler": True,
        "is_adult": False
    },
    {
        "id": 2,
        "name": "Cat Facts",
        "description": "Get random cat facts.",
        "endpoint": "https://catfact.ninja/fact",
        "parameters": [],
        "why_use": "Learn JSON parsing and handling text responses from APIs.",
        "how_use": "Simple GET request returns random cat facts - ideal first API for beginners. No authentication required.",
        "category": "Fun",
        "has_handler": True,
        "is_adult": False
    },
    {
        "id": 3,
        "name": "OpenWeatherMap",
        "description": "Get current weather data.",
        "endpoint": "https://api.openweathermap.org/data/2.5/weather",
        "parameters": [
            {"name": "q", "label": "City", "type": "text", "required": True},
            {"name": "appid", "label": "API Key", "type": "text", "required": True}
        ],
        "why_use": "Learn how to work with APIs that require authentication and handle query parameters.",
        "how_use": "Demonstrates API key usage and parameter passing. Common in weather apps, travel sites, and IoT projects.",
        "category": "Data",
        "has_handler": False,
        "is_adult": False
    },
    {
        "id": 4,
        "name": "Advice Slip",
        "description": "Random life advice.",
        "endpoint": "https://api.adviceslip.com/advice",
        "parameters": [],
        "why_use": "Simple API perfect for practicing JSON data extraction and response handling.",
        "how_use": "Returns motivational advice - great for learning apps, bots, or daily inspiration features.",
        "category": "Fun",
        "has_handler": True,
        "is_adult": True,
        "adult_warning": "This API may contain advice with adult language or mature themes."
    },
    {
        "id": 5,
        "name": "JokeAPI",
        "description": "Programming and general jokes.",
        "endpoint": "https://v2.jokeapi.dev/joke",
        "parameters": [
            {
                "name": "category",
                "label": "Category",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "programming", "label": "Programming"},
                    {"value": "misc", "label": "Miscellaneous"},
                    {"value": "pun", "label": "Pun"},
                    {"value": "spooky", "label": "Spooky"},
                    {"value": "christmas", "label": "Christmas"}
                ]
            },
            {
                "name": "type",
                "label": "Type",
                "type": "select",
                "required": False,
                "options": [
                    {"value": "single", "label": "Single"},
                    {"value": "twopart", "label": "Two-Part"}
                ]
            }
        ],
        "why_use": "Learn parameter handling with dropdown options and conditional response structures.",
        "how_use": "Popular for Slack bots, Discord bots, and entertainment apps. Shows how to handle multiple response formats.",
        "category": "Fun",
        "has_handler": True,
        "is_adult": True,
        "adult_warning": "This API may return jokes with adult language or themes."
    },
    {
        "id": 6,
        "name": "CoinGecko",
        "description": "Cryptocurrency prices and info.",
        "endpoint": "https://api.coingecko.com/api/v3/simple/price",
        "parameters": [
            {
                "name": "ids",
                "label": "Coin",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "bitcoin", "label": "Bitcoin"},
                    {"value": "ethereum", "label": "Ethereum"},
                    {"value": "dogecoin", "label": "Dogecoin"},
                    {"value": "litecoin", "label": "Litecoin"},
                    {"value": "cardano", "label": "Cardano"},
                    {"value": "solana", "label": "Solana"},
                    {"value": "ripple", "label": "Ripple"},
                    {"value": "polkadot", "label": "Polkadot"},
                    {"value": "tron", "label": "Tron"}
                ]
            },
            {
                "name": "vs_currencies",
                "label": "Currency",
                "type": "select",
                "required": True,
                "options": [
                    {"value": "usd", "label": "USD"},
                    {"value": "eur", "label": "EUR"},
                    {"value": "gbp", "label": "GBP"},
                    {"value": "jpy", "label": "JPY"},
                    {"value": "aud", "label": "AUD"}
                ]
            }
        ],
        "why_use": "Practice working with financial data APIs and real-time price information.",
        "how_use": "Used in crypto portfolio trackers, price alert apps, and trading dashboards. No API key required for basic usage.",
        "category": "Cryptocurrency",
        "has_handler": False,
        "is_adult": False
    },
    {
        "id": 7,
        "name": "Genderize",
        "description": "Predict gender from a first name.",
        "endpoint": "https://api.genderize.io",
        "parameters": [
            {"name": "name", "label": "Name", "type": "text", "required": True}
        ],
        "why_use": "Learn about machine learning prediction APIs and probability-based responses.",
        "how_use": "Useful for data analysis, user profiling, and demographic research. Returns gender probability scores.",
        "category": "Data",
        "has_handler": False,
        "is_adult": False
    },
    {
        "id": 8,
        "name": "Agify",
        "description": "Predict age from a name.",
        "endpoint": "https://api.agify.io",
        "parameters": [
            {"name": "name", "label": "Name", "type": "text", "required": True}
        ],
        "why_use": "Understand prediction APIs and statistical estimation from names.",
        "how_use": "Used in demographic analysis, marketing research, and data enrichment tools.",
        "category": "Data",
        "has_handler": False,
        "is_adult": False
    },
    {
        "id": 9,
        "name": "Nationalize",
        "description": "Predict nationality from a name.",
        "endpoint": "https://api.nationalize.io",
        "parameters": [
            {"name": "name", "label": "Name", "type": "text", "required": True}
        ],
        "why_use": "Practice handling multiple prediction results with probability scores.",
        "how_use": "Helps with internationalization, market research, and understanding name origins. Returns multiple country probabilities.",
        "category": "Data",
        "has_handler": False,
        "is_adult": False
    },
    {
        "id": 10,
        "name": "DogAPI",
        "description": "Get random dog facts.",
        "endpoint": "https://dogapi.dog/api/v2/facts",
        "parameters": [],
        "why_use": "Learn to navigate nested JSON responses and extract specific data fields.",
        "how_use": "Great for pet apps, educational content, or practicing JSON parsing with complex structures.",
        "category": "Fun",
        "has_handler": False,
        "is_adult": False
    },
    {
        "id": 11,
        "name": "Numbers API",
        "description": "Trivia and facts about numbers.",
        "endpoint": "http://numbersapi.com/random/trivia",
        "parameters": [],
        "why_use": "Simple text-based API for learning basic HTTP requests and plain text responses.",
        "how_use": "Fun facts for educational apps, trivia games, or daily number facts. Returns plain text instead of JSON.",
        "category": "Fun",
        "has_handler": False,
        "is_adult": False
    },
    {
        "id": 12,
        "name": "OpenLibrary",
        "description": "Book data and cover art.",
        "endpoint": "https://openlibrary.org/search.json",
        "parameters": [
            {"name": "q", "label": "Search Query", "type": "text", "required": True}
        ],
        "why_use": "Practice working with large, complex JSON responses and search functionality.",
        "how_use": "Essential for book apps, library systems, reading trackers, and educational projects. Free and extensive book database.",
        "category": "Data",
        "has_handler": False,
        "is_adult": False
    },
    {
        "id": 13,
        "name": "Kanye Rest",
        "description": "Get a random Kanye West quote.",
        "endpoint": "https://api.kanye.rest",
        "parameters": [],
        "why_use": "Extremely simple API perfect for your very first API call - just one endpoint, no parameters.",
        "how_use": "Popular for meme apps, quote generators, and teaching API basics. Instant success guaranteed!",
        "category": "Fun",
        "has_handler": True,
        "is_adult": True,
        "adult_warning": "Some quotes may contain strong language or mature themes."
    },
    {
        "id": 14,
        "name": "Dad Jokes",
        "description": "Get a dad joke.",
        "endpoint": "https://icanhazdadjoke.com/",
        "parameters": [],
        "why_use": "Learn about content negotiation - API returns different formats based on Accept header.",
        "how_use": "Common in Slack bots, entertainment apps, and icebreaker tools. Shows how headers affect API responses.",
        "category": "Fun",
        "has_handler": False,
        "is_adult": True,
        "adult_warning": "Some jokes may contain mild adult humor."
    }
]


def get_all_apis():
    """
    Return all APIs sorted by name.

    Returns:
        list: Sorted list of API dictionaries
    """
    return sorted(APIS, key=lambda x: x['name'])


def get_api_by_id(api_id):
    """
    Get single API by ID.

    Args:
        api_id (int): The API ID to search for

    Returns:
        dict or None: API dictionary if found, None otherwise
    """
    return next((api for api in APIS if api['id'] == api_id), None)


def search_apis(query):
    """
    Search APIs by name or description.

    Args:
        query (str): Search query string

    Returns:
        list: List of matching API dictionaries
    """
    query = query.lower()
    return [
        api for api in APIS
        if query in api['name'].lower() or query in api['description'].lower()
    ]


def get_apis_by_category(category):
    """
    Get all APIs in a specific category.

    Args:
        category (str): Category name (e.g., 'Fun', 'Data', 'Images')

    Returns:
        list: List of APIs in the category
    """
    return [api for api in APIS if api.get('category') == category]


def get_all_categories():
    """
    Get list of unique categories.

    Returns:
        list: Sorted list of category names
    """
    categories = {api.get('category', 'Other') for api in APIS}
    return sorted(categories)

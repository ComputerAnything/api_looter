from app import create_app, db
from app.models import APIModel


def seed_apis():
    apis = [
        # Dog CEO API
        APIModel(
            name="Dog CEO",
            description="Random pictures of dogs.",
            endpoint="https://dog.ceo/api/breeds/image/random",
            parameters=[]
        ),
        # Cat Facts API
        APIModel(
            name="Cat Facts",
            description="Get random cat facts.",
            endpoint="https://catfact.ninja/fact",
            parameters=[]
        ),
        # OpenWeatherMap API
        APIModel(
            name="OpenWeatherMap",
            description="Get current weather data.",
            endpoint="https://api.openweathermap.org/data/2.5/weather",
            parameters=[
                {"name": "q", "label": "City", "type": "text", "required": True},
                {"name": "appid", "label": "API Key", "type": "text", "required": True}
            ]
        ),
        # Advice Slip API
        APIModel(
            name="Advice Slip",
            description="Random life advice.",
            endpoint="https://api.adviceslip.com/advice",
            parameters=[]
        ),
        # JokeAPI
        APIModel(
            name="JokeAPI",
            description="Programming and general jokes.",
            endpoint="https://v2.jokeapi.dev/joke",
            parameters=[
                {
                    "name": "category",
                    "label": "Category",
                    "type": "select",
                    "required": True,
                    "options": [
                        {"value": "programming", "label": "Programming"},
                        {"value": "misc", "label": "Miscellaneous"},
                        {"value": "dark", "label": "Dark"},
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
            ]
        ),
        # CoinGecko API
        APIModel(
            name="CoinGecko",
            description="Cryptocurrency prices and info.",
            endpoint="https://api.coingecko.com/api/v3/simple/price",
            parameters=[
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
            ]
        ),
        # Genderize API
        APIModel(
            name="Genderize",
            description="Predict gender from a first name.",
            endpoint="https://api.genderize.io",
            parameters=[
                {"name": "name", "label": "Name", "type": "text", "required": True}
            ]
        ),
        # Agify API
        APIModel(
            name="Agify",
            description="Predict age from a name.",
            endpoint="https://api.agify.io",
            parameters=[
                {"name": "name", "label": "Name", "type": "text", "required": True}
            ]
        ),
        # Nationalize API
        APIModel(
            name="Nationalize",
            description="Predict nationality from a name.",
            endpoint="https://api.nationalize.io",
            parameters=[
                {"name": "name", "label": "Name", "type": "text", "required": True}
            ]
        ),
        # DogAPI
        APIModel(
            name="DogAPI",
            description="Get random dog facts.",
            endpoint="https://dogapi.dog/api/v2/facts",
            parameters=[]
        ),
        # Numbers API
        APIModel(
            name="Numbers API",
            description="Trivia and facts about numbers.",
            endpoint="http://numbersapi.com/random/trivia",
            parameters=[]
        ),
        # Open Library API
        APIModel(
            name="OpenLibrary",
            description="Book data and cover art.",
            endpoint="https://openlibrary.org/search.json",
            parameters=[
                {"name": "q", "label": "Search Query", "type": "text", "required": True}
            ]
        ),
        # Kanye Rest API
        APIModel(
            name="Kanye Rest",
            description="Get a random Kanye West quote.",
            endpoint="https://api.kanye.rest",
            parameters=[]
        ),
        # Dad Jokes API
        APIModel(
            name="Dad Jokes",
            description="Get a dad joke.",
            endpoint="https://icanhazdadjoke.com/",
            parameters=[]
        ),
    ]
    db.session.bulk_save_objects(apis)
    db.session.commit()
    print("Database seeded with APIs.")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_apis()

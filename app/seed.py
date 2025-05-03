# pyright: reportCallIssue=false

from app import create_app, db
from app.models import APIModel


def seed_apis():
    apis = [
        APIModel(
            name="Dog CEO",
            description="Random pictures of dogs.",
            endpoint="https://dog.ceo/api/breeds/image/random",
            parameters=[]
        ),
        APIModel(
            name="Cat Facts",
            description="Get random cat facts.",
            endpoint="https://catfact.ninja/fact",
            parameters=[]
        ),
        APIModel(
            name="OpenWeatherMap",
            description="Get current weather data.",
            endpoint="https://api.openweathermap.org/data/2.5/weather",
            parameters=[
                { "name": "q", "label": "City", "type": "text", "required": True },
                { "name": "appid", "label": "API Key", "type": "text", "required": True }
            ]
        ),
        APIModel(
            name="Advice Slip",
            description="Random life advice.",
            endpoint="https://api.adviceslip.com/advice",
            parameters=[]
        ),
        APIModel(
            name="JokeAPI",
            description="Programming and general jokes.",
            endpoint="https://v2.jokeapi.dev/joke/Programming",
            parameters=[
                { "name": "type", "label": "Type (single, twopart)", "type": "text", "required": False }
            ]
        ),
        APIModel(
            name="BoredAPI",
            description="Get activity suggestions when you're bored.",
            endpoint="https://www.boredapi.com/api/activity",
            parameters=[]
        ),
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
                    "label": "Currency (e.g., usd)",
                    "type": "text",
                    "required": True
                }
            ]
        ),
        APIModel(
            name="Genderize",
            description="Predict gender from a first name.",
            endpoint="https://api.genderize.io",
            parameters=[
                { "name": "name", "label": "Name", "type": "text", "required": True }
            ]
        ),
        APIModel(
            name="Agify",
            description="Predict age from a name.",
            endpoint="https://api.agify.io",
            parameters=[
                { "name": "name", "label": "Name", "type": "text", "required": True }
            ]
        ),
        APIModel(
            name="Nationalize",
            description="Predict nationality from a name.",
            endpoint="https://api.nationalize.io",
            parameters=[
                { "name": "name", "label": "Name", "type": "text", "required": True }
            ]
        ),
        APIModel(
            name="IPify",
            description="Get your public IP address.",
            endpoint="https://api.ipify.org",
            parameters=[
                { "name": "format", "label": "Response Format (json, text)", "type": "text", "required": False }
            ]
        ),
        APIModel(
            name="Numbers API",
            description="Trivia and facts about numbers.",
            endpoint="http://numbersapi.com/random/trivia",
            parameters=[]
        ),
        APIModel(
            name="OpenLibrary",
            description="Book data and cover art.",
            endpoint="https://openlibrary.org/search.json",
            parameters=[
                { "name": "q", "label": "Search Query", "type": "text", "required": True }
            ]
        ),
        APIModel(
            name="Kanye Rest",
            description="Get a random Kanye West quote.",
            endpoint="https://api.kanye.rest",
            parameters=[]
        ),
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

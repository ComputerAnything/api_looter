from app import create_app, db
from app.models import APIModel

def seed_apis():
    apis = [
        APIModel(
            name="Cat Facts",
            description="Random cat facts",
            endpoint="https://catfact.ninja/fact",
            parameters=[]
        ),
        APIModel(
            name="Dog CEO",
            description="Random dog images",
            endpoint="https://dog.ceo/api/breeds/image/random",
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

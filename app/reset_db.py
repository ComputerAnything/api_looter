from app import create_app, db
from app.models import APIModel

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


app = create_app()
with app.app_context():
    db.session.query(APIModel).delete()
    db.session.commit()
    print("All APIs have been removed from the database.")

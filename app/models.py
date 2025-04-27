from . import db

class APIModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    endpoint = db.Column(db.String(200), nullable=False)
    parameters = db.Column(db.JSON, nullable=True)
    api_key = db.Column(db.String(255), nullable=True)  # <-- Add this line

    def __repr__(self):
        return f'<APIModel {self.name}>'

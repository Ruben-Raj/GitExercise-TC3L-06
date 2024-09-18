from app import db

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    available_slots = db.Column(db.String(200), nullable=False)  # Storing as a string for simplicity

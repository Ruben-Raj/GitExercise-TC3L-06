from app import db

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    available_slots = db.Column(db.String(200), nullable=False)  # Storing available slots as a string
    gmeet_links = db.Column(db.String(200), nullable=False)  # Store Google Meet links

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    slot = db.Column(db.String(100), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    tutor = db.relationship('Tutor', backref='bookings')

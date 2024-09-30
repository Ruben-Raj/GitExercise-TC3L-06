from app import db

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    available_slots = db.Column(db.String(200), nullable=False)  # Storing as a string for simplicity
    bookings = db.relationship('Booking', back_populates='tutor')

# Booking Model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Associate booking with the user
    slot = db.Column(db.String(100), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)

    student = db.relationship('User', back_populates='bookings')
    tutor = db.relationship('Tutor', back_populates='bookings')
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///slots.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Slot model
class Slot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(10), nullable=True)  # None, "Booked"

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    slots = Slot.query.all()
    return render_template('index.html', slots=slots)

@app.route('/create', methods=['GET', 'POST'])
def create_slot():
    if request.method == 'POST':
        slot_time = request.form.get('slot_time')
        if slot_time:
            existing_slot = Slot.query.filter_by(time=slot_time).first()
            if existing_slot is None:
                new_slot = Slot(time=slot_time, status=None)
                db.session.add(new_slot)
                db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/book/<int:slot_id>', methods=['GET', 'POST'])
def book(slot_id):
    slot = Slot.query.get_or_404(slot_id)
    if request.method == 'POST':
        if slot.status is None:
            slot.status = "Booked"
            db.session.commit()
        return redirect(url_for('index'))
    return render_template('book.html', slot=slot)

if __name__ == '__main__':
    app.run(debug=True)

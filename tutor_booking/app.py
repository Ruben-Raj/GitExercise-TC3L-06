from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///combined.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

# Tutor Model
class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    available_slots = db.Column(db.String(200), nullable=False)

# Booking Model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    slot = db.Column(db.String(100), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.id'), nullable=False)
    tutor = db.relationship('Tutor', backref='bookings')

# Tutor Form
class TutorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    available_slots = StringField('Available Slots (comma-separated)', validators=[DataRequired()])
    submit = SubmitField('Add/Update Tutor')

# Booking Form
class BookingForm(FlaskForm):
    student_name = StringField('Your Name', validators=[DataRequired()])
    slot = StringField('Slot', validators=[DataRequired()])
    submit = SubmitField('Book Slot')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Both username and password are required.', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists, please choose a different one.', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Both username and password are required.', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    search_query = request.args.get('search', '')
    if search_query:
        tutors = Tutor.query.filter(
            (Tutor.name.ilike(f'%{search_query}%')) | 
            (Tutor.subject.ilike(f'%{search_query}%'))
        ).all()
    else:
        tutors = Tutor.query.all()
    return render_template('home.html', tutors=tutors)

@app.route('/tutor/<int:tutor_id>')
def tutor_info(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)
    return render_template('tutor_info.html', tutor=tutor)

@app.route('/add_tutor', methods=['GET', 'POST'])
def add_tutor():
    form = TutorForm()
    if form.validate_on_submit():
        tutor = Tutor(name=form.name.data, phone=form.phone.data, subject=form.subject.data,
                      available_slots=form.available_slots.data)
        db.session.add(tutor)
        db.session.commit()
        flash('Tutor added/updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_tutor.html', form=form)

@app.route('/edit_tutor/<int:tutor_id>', methods=['GET', 'POST'])
def edit_tutor(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)
    form = TutorForm(obj=tutor)
    if form.validate_on_submit():
        tutor.name = form.name.data
        tutor.phone = form.phone.data
        tutor.subject = form.subject.data
        tutor.available_slots = form.available_slots.data
        db.session.commit()
        flash('Tutor updated successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('edit_tutor.html', form=form, tutor=tutor)

@app.route('/delete_tutor/<int:tutor_id>', methods=['POST'])
def delete_tutor(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)
    db.session.delete(tutor)
    db.session.commit()
    flash('Tutor deleted successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/book/<int:tutor_id>', methods=['GET', 'POST'])
def book_slot(tutor_id):
    tutor = Tutor.query.get_or_404(tutor_id)
    form = BookingForm()
    if form.validate_on_submit():
        selected_slot = form.slot.data.strip()
        slots = [slot.strip() for slot in tutor.available_slots.split(',')]
        if selected_slot in slots:
            slots.remove(selected_slot)
            tutor.available_slots = ', '.join(slots)
            booking = Booking(student_name=form.student_name.data, slot=selected_slot, tutor_id=tutor_id)
            db.session.add(booking)
            db.session.commit()
            flash('Slot booked successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Slot not available!', 'danger')
    return render_template('book_slot.html', tutor=tutor, form=form)

@app.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    tutor = Tutor.query.get(booking.tutor_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        flash('Booking cancelled successfully!', 'success')
        return redirect(url_for('view_bookings'))
    flash('Error cancelling booking.', 'danger')
    return redirect(url_for('view_bookings'))

@app.route('/view_bookings')
def view_bookings():
    bookings = Booking.query.all()
    return render_template('view_bookings.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)

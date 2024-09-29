from app import app, db

# Create the database and the tables within the application context
with app.app_context():
    db.create_all()

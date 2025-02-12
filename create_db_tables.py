from app import app, db

with app.app_context():
    """Creates an empty table for each of the database models"""
    db.create_all()
    print('Tables created successfully')
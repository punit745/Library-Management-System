"""
Initialize the database by creating all tables
"""
from app import app
from models import db

def init_database():
    """Create all database tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    init_database()

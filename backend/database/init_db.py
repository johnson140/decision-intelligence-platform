"""
Initialize the database - creates all tables.
Runs the file once to set up your database structure.
"""

from database.connection import engine
from database.models import Base

def init_database():
    """
    Create all tables defined in models.py
    """
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully!")

if __name__ == "__main__":
    init_database()
"""
Database connection and session management.
This file handles connecting Python to PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Create the database engine
# The engine is the "low-level connection" to PostgreSQL
# echo=True will print SQL queries to the console 
# helpful for debugging
engine = create_engine(
    settings.DATABASE_URL,
    echo=True  # Change to False in production
)

# Create a SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,  # Don't save automatically 
    autoflush=False,   # Don't send changes automatically
    bind=engine        # This session talks to PostgreSQL database
)


def get_db():
    """
    This function gives you a database session.
    Use it whenever you need to read or write to the database.
    
    It automatically closes the session when you're done .
    """
    db = SessionLocal()
    try:
        yield db  # This gives the session to whoever called this function
    finally:
        db.close()  # Always close the session when done
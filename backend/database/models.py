"""
Database table definitions for Decision Intelligence Platform.
These classes tell SQLAlchemy what tables to create in PostgreSQL.
"""

# Import tools from SQLAlchemy that we need
# Each import is a "building block" for defining tables


from sqlalchemy import (
    Column,          # Defines a column in a table
    Integer,         # Whole numbers: 1, 2, 50, 100
    String,          # Text with a max length: "Widget A"
    Float,           # Decimal numbers: 10.50, 25.99
    DateTime,        # Dates and times: 2024-01-15 10:30:00
    ForeignKey,      # Links two tables together 
    Text             # Long text with no length limit
)


from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


# This is the base class. Every table class created
# will inherit from this. 

class Base(DeclarativeBase):
    pass



# TABLE 1: Products
# Stores information about each product

class Product(Base):  
   
    __tablename__ = "products" # create a table called 'products'

    # Each line below is one column in the table
    # product_id is the PRIMARY KEY - unique identifier, auto-increments
    product_id = Column(Integer, primary_key=True, autoincrement=True)

    # product_name - text, max 255 characters, cannot be empty
    product_name = Column(String(255), nullable=False)

    # unit_price - decimal number, how much one item costs, cannot be empty
    unit_price = Column(Float, nullable=False)

    # current_stock - how many items are in the shop right now
    # starts at 0 when a product is first added
    current_stock = Column(Integer, default=0)

    # created_at - automatically records WHEN this product was first added
    # default=datetime.utcnow means it fills itself automatically
    created_at = Column(DateTime, default=datetime.utcnow)



# TABLE 2: Transactions
# Stores every single sale that happens

class Transaction(Base):
     # create a table called 'transactions'"
    __tablename__ = "transactions"

    # transaction_id - unique identifier for each sale, auto-increments
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)

    # product_id - this links to the Products table
    # ForeignKey means: "this number must exist in products.product_id"    
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)

    # quantity - how many items were sold in this transaction
    quantity = Column(Integer, nullable=False)

    # unit_price - the price at the time of sale
    # (price can change over time, so we store it here too)
    unit_price = Column(Float, nullable=False)

    # transaction_date - when did this sale happen
    transaction_date = Column(DateTime, nullable=False)

    # customer_id - optional, who bought it
    # nullable=True means this column CAN be empty
    customer_id = Column(String(100), nullable=True)

    # created_at - when was this record added to the database
    created_at = Column(DateTime, default=datetime.utcnow)
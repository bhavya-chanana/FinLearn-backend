from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime, ARRAY, CheckConstraint, MetaData, select, insert, update, delete
from datetime import datetime
from config import Config
from databases import Database


DATABASE_URL = "postgresql://postgres:Qwerty11@@localhost:5432/finance_app"

# Initialize database connection
database = Database(DATABASE_URL)
metadata = MetaData()

# Define the expenses table
expenses_table = Table('expenses', metadata,
    Column('id', Integer, primary_key=True),
    Column('amount', Float, nullable=False),
    Column('category', String(50)),
    Column('payment_mode', String(50), nullable=False),
    Column('description', String),
    Column('tags', ARRAY(String)),
    Column('date', DateTime, default=datetime.utcnow),
    CheckConstraint(
        "payment_mode IN ('cash', 'upi', 'debit/credit card', 'bank transfer')",
        name='check_payment_mode'
    )
)


# Function to add a new expense
def add_expense(data):
    ins = expenses_table.insert().values(
        amount=data['amount'],
        category=data.get('category', ''),
        payment_mode=data['payment_mode'],
        description=data.get('description', ''),
        tags=data.get('tags', []),
        date=datetime.utcnow()
    )
    result = connection.execute(ins)
    return result.inserted_primary_key[0]

# Function to get all expenses
def get_expenses():
    sel = select([expenses_table]).order_by(expenses_table.c.date.desc())
    result = connection.execute(sel)
    return [dict(row) for row in result]

# Function to update an expense
def update_expense(id, data):
    upd = expenses_table.update().where(expenses_table.c.id == id).values(
        amount=data.get('amount'),
        category=data.get('category'),
        payment_mode=data.get('payment_mode'),
        description=data.get('description'),
        tags=data.get('tags')
    )
    result = connection.execute(upd)
    return result.rowcount

# Function to delete an expense
def delete_expense(id):
    delete_stmt = expenses_table.delete().where(expenses_table.c.id == id)
    result = connection.execute(delete_stmt)
    return result.rowcount

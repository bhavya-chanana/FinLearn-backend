import psycopg2
from psycopg2.extras import RealDictCursor

# Function to establish connection to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="finance_app",
        user="postgres",
        password="Qwerty11@"
    )
    return conn

# Function to retrieve all expenses from the database
def get_expenses():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()
    cursor.close()
    conn.close()
    return expenses

# Function to add a new expense to the database
def add_expense(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses (amount, category, payment_mode, description, tags, date)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
        """,
        (data['amount'], data['category'], data['payment_mode'], data.get('description', ''),
         data.get('tags', []), data['date'])
    )
    conn.commit()
    expense_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return {'status': 'success', 'id': expense_id}

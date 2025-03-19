import mysql.connector
from contextlib import contextmanager

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host= "localhost",
        user = "root",
        password = "root",
        database= "expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        connection.commit()

    cursor.close()
    connection.close()

def fetch_all_records():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses;")
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)

def delete_expenses_for_date(expense_date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expense_manager.expenses WHERE expense_date = %s", (expense_date,))

def fetch_expenses_for_date(expense_date):
    with get_db_cursor() as cursor:
        query = "SELECT amount, category, notes FROM expenses WHERE expense_date = %s"
        cursor.execute(query, (expense_date,))
        expenses = cursor.fetchall()
    return expenses

def insert_expenses(expense_date, amount, category, notes):
    query = "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)"
    try:
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(query, (expense_date, amount, category, notes))
    except Exception as e:
        print(f"Error inserting expense: {e}")  # Handle exceptions properly

def fetch_expense_summery(start_date, end_date):
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total FROM expenses where expense_date BETWEEN %s AND %s GROUP BY category''', (start_date, end_date)
        )
        data = cursor.fetchall()
        return data


def fetch_expenses_by_month_range(start_date, end_date):
    """Fetches expense summary for a given month range."""

    formatted_start_date = start_date[:7]  # Extract YYYY-MM only
    formatted_end_date = end_date[:7]  # Extract YYYY-MM only

    query = """
        SELECT category, SUM(amount) as total FROM expenses 
        WHERE DATE_FORMAT(expense_date, '%Y-%m') BETWEEN %s AND %s 
        GROUP BY category
    """

    with get_db_cursor() as cursor:
        print(f"DEBUG: Fetching data for range {formatted_start_date} to {formatted_end_date}")  # ✅ Debug log
        cursor.execute(query, (formatted_start_date, formatted_end_date))
        data = cursor.fetchall()
        print(f"DEBUG: Fetched data: {data}")  # ✅ Debug log
        return data

if __name__ == "__main__":
    #insert_expenses("2024-08-10", 100.50, "Food", "Biriyani")
    #fetch_expenses_for_date("2024-08-10")
    summery = fetch_expenses_by_month_range('2024-08-01', '2024-12-31')
    for line in summery:
        print(line)

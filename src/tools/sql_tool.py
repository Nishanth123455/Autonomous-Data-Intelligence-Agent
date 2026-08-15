from pathlib import Path
import sqlite3
import pandas as pd


def load_dataset_to_sqlite(csv_path, database_path):
    """
    Load the CSV dataset into a SQLite database.
    """

    csv_path = Path(csv_path)
    database_path = Path(database_path)

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}"
        )

    database_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df = pd.read_csv(csv_path)

    connection = sqlite3.connect(database_path)

    df.to_sql(
        "sales",
        connection,
        if_exists="replace",
        index=False
    )

    connection.close()


def run_sql_query(database_path, query):
    """
    Execute a read-only SQL query and return the result.
    """

    database_path = Path(database_path)

    if not database_path.exists():
        raise FileNotFoundError(
            f"Database not found: {database_path}"
        )

    # Basic safety check
    forbidden = [
        "insert ",
        "update ",
        "delete ",
        "drop ",
        "alter ",
        "create ",
        "replace ",
        "truncate "
    ]

    query_lower = query.lower()

    for keyword in forbidden:
        if keyword in query_lower:
            raise ValueError(
                "Only read-only SQL queries are allowed."
            )

    connection = sqlite3.connect(database_path)

    try:
        result = pd.read_sql_query(
            query,
            connection
        )
    finally:
        connection.close()

    return result


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    csv_path = (
        project_root
        / "data"
        / "processed"
        / "cleaned_sales_data.csv"
    )

    database_path = (
        project_root
        / "data"
        / "processed"
        / "sales.db"
    )

    # Load dataset into SQLite
    load_dataset_to_sqlite(
        csv_path,
        database_path
    )

    print("\n===== SQL TOOL =====")

    print("\nDatabase created:")
    print(database_path)

    # Test 1: Total revenue
    query = """
    SELECT SUM(revenue) AS total_revenue
    FROM sales
    """

    result = run_sql_query(
        database_path,
        query
    )

    print("\nTotal Revenue:")
    print(result)

    # Test 2: Revenue by region
    query = """
    SELECT
        region,
        SUM(revenue) AS total_revenue
    FROM sales
    GROUP BY region
    ORDER BY total_revenue DESC
    """

    result = run_sql_query(
        database_path,
        query
    )

    print("\nRevenue by Region:")
    print(result)

    # Test 3: Q3 revenue by region
    query = """
    SELECT
        region,
        SUM(revenue) AS q3_revenue
    FROM sales
    WHERE CAST(
        strftime('%m', order_date)
        AS INTEGER
    ) BETWEEN 7 AND 9
    GROUP BY region
    ORDER BY q3_revenue DESC
    """

    result = run_sql_query(
        database_path,
        query
    )

    print("\nQ3 Revenue by Region:")
    print(result)
from pathlib import Path

from src.load.db_connection import get_connection


BASE_DIR = Path(__file__).resolve().parents[2]
SQL_DIR = BASE_DIR / "sql"


def execute_sql_file(cursor, filename):
    sql_path = SQL_DIR / filename
    sql = sql_path.read_text(encoding="utf-8")

    if not sql.strip():
        raise ValueError(f"SQL file is empty: {sql_path}")

    cursor.execute(sql)
    print(f"Executed {filename}")


def setup_database():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            execute_sql_file(cursor, "schema.sql")
            execute_sql_file(cursor, "transform.sql")

        connection.commit()
        print("Database setup completed successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    setup_database()
import sqlite3
from pathlib import Path

import pandas as pd


DATABASE_PATH = Path("data/erp_orders.db")
CSV_PATH = Path("data/erp_orders.csv")


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_database():
    df = pd.read_csv(CSV_PATH)

    DATABASE_PATH.parent.mkdir(exist_ok=True)

    connection = get_connection()

    df.to_sql(
        "orders",
        connection,
        if_exists="replace",
        index=False,
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS exception_resolutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            exception_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            action_taken TEXT,
            resolved_at TEXT
        )
        """
    )

    connection.commit()
    connection.close()

    print(f"Database created at {DATABASE_PATH}")


def create_resolution_table():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS exception_resolutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            exception_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            action_taken TEXT,
            resolved_at TEXT
        )
        """
    )

    connection.commit()
    connection.close()


def save_resolution(
    order_id,
    exception_type,
    status,
    action_taken,
):
    create_resolution_table()

    connection = get_connection()

    existing = connection.execute(
        """
        SELECT id
        FROM exception_resolutions
        WHERE order_id = ?
        AND exception_type = ?
        """,
        (order_id, exception_type),
    ).fetchone()

    resolved_at = None

    if status == "Resolved":
        resolved_at = pd.Timestamp.now().isoformat()

    if existing:
        connection.execute(
            """
            UPDATE exception_resolutions
            SET status = ?,
                action_taken = ?,
                resolved_at = ?
            WHERE id = ?
            """,
            (
                status,
                action_taken,
                resolved_at,
                existing[0],
            ),
        )

    else:
        connection.execute(
            """
            INSERT INTO exception_resolutions (
                order_id,
                exception_type,
                status,
                action_taken,
                resolved_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                order_id,
                exception_type,
                status,
                action_taken,
                resolved_at,
            ),
        )

    connection.commit()
    connection.close()


def get_resolutions():
    create_resolution_table()

    connection = get_connection()

    df = pd.read_sql_query(
        """
        SELECT *
        FROM exception_resolutions
        ORDER BY id DESC
        """,
        connection,
    )

    connection.close()

    return df


def clear_resolutions():
    create_resolution_table()

    connection = get_connection()

    connection.execute(
        "DELETE FROM exception_resolutions"
    )

    connection.commit()
    connection.close()


def run_query(query):
    connection = get_connection()

    df = pd.read_sql_query(
        query,
        connection,
    )

    connection.close()

    return df


if __name__ == "__main__":
    create_database()
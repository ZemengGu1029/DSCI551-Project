import os
import sqlite3
import time
import random
from datetime import datetime, timedelta

DB_NAME = "demo.db"


def reset_database(db_name: str = DB_NAME) -> None:
    """Delete old database so every demo starts from a clean state."""
    if os.path.exists(db_name):
        os.remove(db_name)


def connect_db(db_name: str = DB_NAME) -> sqlite3.Connection:
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn


def create_schema(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            status TEXT,
            due_date TEXT,
            title TEXT
        )
    """)


def insert_sample_data(cursor: sqlite3.Cursor, n: int = 10000) -> None:
    random.seed(42)

    statuses = ["open", "completed"]
    titles = ["Task", "Demo prep", "Report writing", "Slide review"]

    start_date = datetime(2026, 3, 1)
    data = []

    for i in range(n):
        status = random.choice(statuses)
        due_date = start_date + timedelta(days=random.randint(0, 60))
        title = f"{random.choice(titles)} {i}"
        data.append((status, due_date.strftime("%Y-%m-%d"), title))

    cursor.executemany(
        "INSERT INTO tasks (status, due_date, title) VALUES (?, ?, ?)",
        data
    )


def print_plan(cursor: sqlite3.Cursor, sql: str) -> None:
    cursor.execute(f"EXPLAIN QUERY PLAN {sql}")
    plan_rows = cursor.fetchall()

    print("EXPLAIN QUERY PLAN:")
    for row in plan_rows:
        print(f"  - {row[3]}")


def run_and_time_query(cursor: sqlite3.Cursor, sql: str) -> tuple[int, float]:
    start = time.perf_counter()
    cursor.execute(sql)
    rows = cursor.fetchall()
    elapsed = time.perf_counter() - start
    return len(rows), elapsed


def explain_and_run(
    cursor,
    title,
    application_desc,
    sql,
    internal_desc,
    why_it_matters
):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(f"Application behavior: {application_desc}")
    print(f"Database internal behavior: {internal_desc}")
    print(f"Why it matters: {why_it_matters}\n")

    print_plan(cursor, sql)
    count, elapsed = run_and_time_query(cursor, sql)
    print(f"Returned {count} rows")
    print(f"Execution time: {elapsed:.6f} seconds")


def pause(step_name: str) -> None:
    input(f"\n--- {step_name} (Press Enter to continue) ---")

# %% Part 1: Create database and load synthetic data
def main():
    reset_database()

    conn = connect_db()
    cursor = conn.cursor()

    print("Creating database and table...")
    create_schema(cursor)
    conn.commit()

    print("Inserting 10,000 sample records...")
    insert_sample_data(cursor, n=10000)
    conn.commit()
    print("Data insertion completed.")


# %% Part 2: Operation 1: Query without index
    pause("Operation 1: Full Table Scan")

    explain_and_run(
        cursor,
        "Operation 1: Query without index (Full Table Scan)",
        "Retrieve all tasks with status = 'open'",
        "SELECT * FROM tasks WHERE status = 'open'",
        "SQLite performs SCAN tasks, traversing the entire B-tree",
        "Without an index, SQLite must check every row, which is inefficient for large datasets."
    )


# %% Part 3: Create single-column index and run Operation 2
    pause("Create Single-Column Index")

    print("\nCreating single-column index idx_status...")
    cursor.execute("CREATE INDEX idx_status ON tasks(status)")
    conn.commit()
    print("Index created.")

    pause("Operation 2: Index Scan")

    explain_and_run(
        cursor,
        "Operation 2: Query with index (Index Scan)",
        "Retrieve all tasks with status = 'open'",
        "SELECT * FROM tasks WHERE status = 'open'",
        "SQLite performs SEARCH USING INDEX idx_status (B-tree traversal)",
        "The index allows SQLite to directly locate matching rows, reducing page access."
    )


# %% Part 4: Operation 3: Filtering + ordering with single-column index
    pause("Operation 3: Filtering + Ordering")

    explain_and_run(
        cursor,
        "Operation 3: Filtering + Ordering (Single-column index limitation)",
        "Retrieve 'open' tasks ordered by due_date",
        "SELECT * FROM tasks WHERE status = 'open' ORDER BY due_date",
        "SQLite uses index for filtering but builds a temporary B-tree for sorting",
        "Single-column index cannot support both filtering and ordering, causing extra overhead."
    )


# %% Part 5: Create composite index and run Operation 4
    pause("Create Composite Index")

    print("\nCreating composite index idx_status_due...")
    cursor.execute("CREATE INDEX idx_status_due ON tasks(status, due_date)")
    conn.commit()
    print("Composite index created.")

    pause("Operation 4: Composite Index Optimization")

    explain_and_run(
        cursor,
        "Operation 4: Composite Index Optimization",
        "Retrieve 'open' tasks ordered by due_date",
        "SELECT * FROM tasks WHERE status = 'open' ORDER BY due_date",
        "SQLite uses composite index for a single B-tree traversal",
        "Composite index eliminates the need for temporary sorting and improves efficiency."
    )

    conn.close()
    print("\nDemo completed.")


if __name__ == "__main__":
    main()


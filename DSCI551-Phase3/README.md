# SQLite Task Management Demo (DSCI 551 Project)
## Overview
This project demonstrates how database internals affect application behavior using SQLite.

A Python-based task management application is implemented to analyze how different indexing strategies influence query execution plans, including:
- Full table scan (SCAN)
- Index-based search (SEARCH)
- Temporary B-tree for sorting
- Composite index optimization
---

## Environment Setup
Python 3.14.0

## Install Dependencies
No external dependencies are required.
The project only uses built-in Python libraries:
- sqlite3
- time
- random
- datetime
---

## Project Configuration
No manual configuration is needed.
The script automatically:
- Creates a SQLite database file (demo.db)
- Defines the database schema
- Generates synthetic data
- Creates indexes during execution
---

## How to Run the Application
1. Clone the repository:
git clone https://github.com/ZemengGu1029/DSCI551-Project.git
cd DSCI551-Project
2. Run the script: python project.py
## What Happens When You Run the Script
The script performs the following steps automatically:
1. Deletes any existing database file (`demo.db`)
2. Creates a new SQLite database
3. Creates the `tasks` table
4. Generates 10,000 synthetic task records
5. Inserts data into the database
6. Executes multiple queries to demonstrate:
   - Full table scan (SCAN)
   - Index-based search (SEARCH)
   - Sorting with temporary B-tree
   - Composite index optimization
7. Displays execution plans using `EXPLAIN QUERY PLAN`
8. Prints execution time and results
---

## Dataset and Data Generation
This project uses synthetic data generated at runtime.
- No external dataset is required
- Data is generated automatically when the script runs
- 10,000 records are inserted into the database

This ensures:
- Reproducibility
- Controlled experiments
- Consistent results
---

## How to Reproduce Results
1. Run the script: `python project.py`
2. Observe the output:
   - Execution plans (SCAN, SEARCH, TEMP B-TREE)
   - Query results
   - Execution time
Each run recreates the database and produces consistent behavior.


## Notes
1. The database file demo.db is automatically recreated each time the script runs
2. No manual setup is required
3. The project is fully self-contained

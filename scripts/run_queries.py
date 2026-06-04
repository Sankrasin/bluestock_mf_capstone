import sqlite3
from pathlib import Path

# =========================
# PATH TO DB
# =========================
project_root = Path(__file__).resolve().parent.parent
db_path = project_root / "data" / "db" / "bluestock_mf.db"

conn = sqlite3.connect(db_path)

# =========================
# LOAD QUERIES
# =========================
queries_file = project_root / "sql" / "queries.sql"

with open(queries_file, "r") as f:
    queries = f.read().split(";")

# =========================
# EXECUTE QUERIES
# =========================
for i, q in enumerate(queries, 1):
    q = q.strip()
    if q:
        print(f"\n--- QUERY {i} ---")
        try:
            result = conn.execute(q).fetchall()
            for row in result[:10]:  # show top 10 rows
                print(row)
        except Exception as e:
            print("Error:", e)

conn.close()
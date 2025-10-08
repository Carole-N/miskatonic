import os 

MDB_CONNECTION = "mongodb://isen:isen@localhost:27017/admin"
MDB_BASE="miskatonic"
MDB_COLLECTION="question"

# --- SQLite ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB = f"sqlite:///{os.path.join(BASE_DIR, '../database/miskatonic_users.db')}"
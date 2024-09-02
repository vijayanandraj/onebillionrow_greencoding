import sqlite3

METRICS_DB = 'data_processing_metrics.db'


def setup_database(db_path=METRICS_DB):
    """
    Sets up the database for storing data processing metrics.

    Args:
    db_path (str): The file path for the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_type TEXT,
        total_emissions REAL,
        emissions_efficiency REAL,
        processing_time REAL,
        memory_usage REAL,
        cpu_utilization REAL,
        yearly_projections REAL
    )
    ''')
    conn.commit()
    conn.close()


def get_connection():
    conn = sqlite3.connect(METRICS_DB)
    return conn

def delete_records():
    conn = get_connection()
    c = conn.cursor()
    c.execute("delete from metrics")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Run the setup function if this script is executed directly
    #setup_database()
    delete_records()
    print("Records Deleted...")

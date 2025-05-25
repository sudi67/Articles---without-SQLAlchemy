import sqlite3

def setup_database():
    conn = sqlite3.connect('articles.db')
    with open('lib/db/schema.sql', 'r') as f:
        schema_sql = f.read()
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Database setup completed.")

if __name__ == "__main__":
    setup_database()

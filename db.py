import sqlite3 as sql


class DbConnection:
    def __init__(self):
        self.con = sql.connect('safetyWatch.db')
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );            
            """)
        self.con.execute("""
            INSERT INTO users (username, password) VALUES ('admin', 'admin');
        """
        )
        self.con.commit()
        self.cur = self.con.cursor()

    def query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def __del__(self):
        self.con.close()

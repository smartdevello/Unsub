import sqlite3
import json
import os


class DB:
    def __init__(self):
        self.abs_path = os.path.abspath(os.path.dirname(__file__))
        self.connection = sqlite3.connect(os.path.join(self.abs_path , 'unsub_emails.db'))
        self.cursor = self.connection.cursor()
        pass
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, tb):
        try:
            self.connection.close()
        except Exception as e:
            pass

    def findRowByEmail(self, email):

        query = "SELECT * FROM unsub_emails WHERE email=?"
        result = self.cursor.execute(query, (email, ))
        row = result.fetchone()

        if row:
            return {'email' : row[0], 'processed' : row[1]}
        else: return None

    def insertRow(self, email, processed):
        query = "INSERT INTO unsub_emails VALUES (?,?)"
        self.cursor.execute(query, (email, processed))
        self.connection.commit()

    def findAllPendingEmails(self):
        query = "SELECT * FROM unsub_emails WHERE processed = 0"
        result = self.cursor.execute(query)
        rows = result.fetchall()
        return rows
    def updateAsProcessed(self, email, processed):
        query = f"UPDATE unsub_emails SET processed = '{processed}' WHERE email = '{email}'"
        self.cursor.execute(query)
        self.connection.commit()
   

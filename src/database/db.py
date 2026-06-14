import sqlite3

from src.config.settings import DATABASE_PATH


class DatabaseManager:

    def __init__(self):
        DATABASE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False
        )

        self.create_tables()

    def create_tables(self):

        cursor = self.connection.cursor()

        # Chat History
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT,
            assistant_response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Tickets
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue TEXT,
            priority TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Feedback
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rating INTEGER,
            comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Documents
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.connection.commit()

    # -----------------------------
    # Documents
    # -----------------------------

    def add_document(self, filename):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO documents(file_name)
            VALUES(?)
            """,
            (filename,)
        )

        self.connection.commit()

    def get_documents(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM documents
            ORDER BY uploaded_at DESC
            """
        )

        return cursor.fetchall()

    # -----------------------------
    # Chat History
    # -----------------------------

    def save_chat(self, question, answer):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO chat_history(
                user_query,
                assistant_response
            )
            VALUES(?, ?)
            """,
            (question, answer)
        )

        self.connection.commit()

    def get_chat_history(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM chat_history
            ORDER BY created_at DESC
            """
        )

        return cursor.fetchall()

    # -----------------------------
    # Tickets
    # -----------------------------

    def create_ticket(
        self,
        issue,
        priority="Medium",
        status="Open"
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO tickets(
                issue,
                priority,
                status
            )
            VALUES(?, ?, ?)
            """,
            (
                issue,
                priority,
                status
            )
        )

        self.connection.commit()

    def get_tickets(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM tickets
            ORDER BY created_at DESC
            """
        )

        return cursor.fetchall()

    # -----------------------------
    # Feedback
    # -----------------------------

    def add_feedback(
        self,
        rating,
        comments
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO feedback(
                rating,
                comments
            )
            VALUES(?, ?)
            """,
            (
                rating,
                comments
            )
        )

        self.connection.commit()

    def get_feedback(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM feedback
            ORDER BY created_at DESC
            """
        )

        return cursor.fetchall()
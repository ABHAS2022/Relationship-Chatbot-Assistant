# import mariadb
# import sys

# # Connect to MariaDB Platform
# try:
#     conn = mariadb.connect(
#         user="root",
#         password="mypass",
#         host="127.0.2.1",
#         port=3306,
#         database="rel_chat_app"
#     )
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")
#     sys.exit(1)

# # Get Cursor
# cur = conn.cursor()
# cur.execute("describe rel_chat_logs")
# print(cur.fetchall())

import sqlalchemy as db
from contextlib import contextmanager
import os

class chatapp:
    def __init__(self, db_port = os.getenv("DB_PORT",33306), db_host = os.getenv("DB_HOST","localhost"), db_user =os.getenv("DB_USER","root"), db_password = os.getenv("DB_PASSWORD","mypass"), db_name = os.getenv("DB_NAME","chatapp")):
        self.db_port = db_port
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        
    def _get_engine(self):
        """Create a database engine."""
        return db.create_engine(f"mariadb+mariadbconnector://{self.db_user}:{self.db_password}@{self.db_host}:{str(self.db_port)}/{self.db_name}")
    
    # @staticmethod
    @contextmanager
    def _connect(self):
        """Context manager for database connection."""
        engine = self._get_engine()
        with engine.connect() as conn:
            yield conn

    


# chat_logs = RelChatLogs()
# with chat_logs._connect() as conn:
#     result = conn.execute(db.text("describe rel_chat_logs"))
#     for row in result:  
#         print(row)

    
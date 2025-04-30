# 



# chat_database.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
import sys
import os
sys.path.append(os.getcwd())
from database.db_model import users, message
from database.db_connector import chatapp  # assuming same connector is used
import os
import sys
from sqlalchemy import and_
sys.path.append(os.getcwd())
import uuid
# from utils import string_to_md5


class ChatAppDatabase:
    def __init__(self, db_connector_class=chatapp()):
        self.engine = db_connector_class._get_engine()
        self.session_factory = sessionmaker(bind=self.engine)
        self.inspector = inspect(self.engine)

    def retrieve_table_names(self):
        """Retrieve all table names from the database."""
        return self.inspector.get_table_names()

    def get_table_info(self, table_name):
        """Describe a given table."""
        if table_name not in self.retrieve_table_names():
            raise ValueError(f"Table {table_name} does not exist.")
        return self.inspector.get_columns(table_name)
    
    # def check_if_user_already_exists(self, name, user_password):
    #     """check if the name and user_password already exists"""
    #     with self.session_factory() as session:
    #         returnn
    

    def add_user(self, name, user_password):
        """Add a user to the users table."""
        if (self.is_user_present(user_password)):
            raise ValueError(f"User with password {user_password} already exists.")
        with self.session_factory() as session:
            user = users(name=name, identification_key_md5 = user_password)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def add_message(self, user_id,  message_text, message_type, user_password, thread_id, message_id = str(uuid.uuid4())):
        """Add a message to the messages table."""
        if not (self.is_user_present(user_password)):
            raise ValueError(f"User with password don't exists.")
        with self.session_factory() as session:
            if not session.query(message).filter_by(message_id=message_id).first() is None:
                # raise ValueError(f"Message with ID {message_id} already exists.")
                return None
            else:
                message_text = message(user_id=user_id, thread_id = thread_id, message_id = message_id, message_text=message_text, message_type=message_type)
                session.add(message_text)
                session.commit()
                session.refresh(message_text)
                return message

    def get_latest_message_by_thread(self, thread_id):
        with self.session_factory() as session:
            latest_message = (
                session.query(message)
                .filter(message.thread_id == thread_id)
                .order_by(message.message_order.desc())
                .first()
            )
            return latest_message.message_text if latest_message else "No messages yet."


    def delete_thread_by_id(self, thread_id):
        with self.session_factory() as session:
            session.query(message).filter(message.thread_id == thread_id).delete()
            session.commit()


    def get_messages_by_user(self, user_id):
        """Fetch all messages by a user ID."""
        with self.session_factory() as session:
            return session.query(message).filter_by(user_id=user_id).all()

    def is_user_present(self, password_md5):
        with self.session_factory() as session:
            return session.query(users).filter(users.identification_key_md5 == password_md5).first() is not None
    
    def get_user_id(self,username ,password):
        """Fetch user ID by password."""
        with self.session_factory() as session:
            user = session.query(users).filter(and_(users.identification_key_md5 == password, users.name == username)).first()
            if user:
                return user.user_id
            else:
                raise ValueError(f"User with password {password} does not exist.")
            

    def user_exists(self, username, password_md5):
        """Check if a user exists by username and password."""
        with self.session_factory() as session:
            user = session.query(users).filter(
                and_(
                    users.name == username,
                    users.identification_key_md5 == password_md5
                )
            ).first()
            
            if user is not None:
                return True
            else:
                return False
            
    def get_messages_by_thread_id(self, thread_id):
        with self.session_factory() as session:
            messages = (
                session.query(message)
                .filter(message.thread_id == thread_id)
                .order_by(message.message_order)  # Ensure chronological order
                .all()
            )
            return messages
    
    def get_threads_by_user(self, user_id):
        with self.session_factory() as session:
            threads = (
                session.query(message.thread_id)
                .filter(message.user_id == user_id)
                .order_by(message.message_order)  # Ensure chronological order
                .distinct()
                .all()
            )
            return [t[0] for t in threads]  # Flatten list of tuples



if __name__ == "__main__":
    db = ChatAppDatabase()

    # Add a message
    # user_id = uuid.UUID("33c23b24-cd0d-47c4-8990-c4f76824ac5e")
    # msg = db.add_message(user_id=user_id, message_id = user_id, message_text="Hello world!", message_type="user")
    # print(f"Message added: {msg}")

    # # Get all messages for that user
    # user_msgs = db.get_messages_by_user(user_id)
    # for m in user_msgs:
    #     print(m.message_text)
    print(db.retrieve_message_from_thread_id(""))
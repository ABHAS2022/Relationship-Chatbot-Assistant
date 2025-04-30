from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, func, TIMESTAMP, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid
import os
import sys
sys.path.append(os.getcwd())
from enums import messageTypeEnum
# from enum import Enum
from sqlalchemy import Enum
import datetime


base = declarative_base()


class users(base):
    __tablename__ = 'users'
    user_id = Column(UUID(as_uuid=True), primary_key=True, default = uuid.uuid4)
    name = Column(String)
    identification_key_md5 = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return f"""<User(name={self.name},"
        "identification_key_md5={self.identification_key_md5})
        name={self.name}, 
        created_at={self.created_at})>"""


class message(base):
    __tablename__ = "messages"
    message_id = Column(String(100), primary_key=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    thread_id = Column(String(100), nullable=True)  # <-- 🆕 Add this line
    message_text = Column(Text, nullable=False)
    message_order = Column(Integer, nullable=False)
    message_type = Column(Enum(messageTypeEnum), default=messageTypeEnum.user)
    created_at = Column(DateTime, default=datetime.datetime.now())
    

    def __repr__(self):
        return f"""<message(message_id={self.message_id}, 
        user_id={self.user_id}, 
        thread_id={self.thread_id}, 
        message_text={self.message_text}, 
        message_type={self.message_type},
        message_id = {self.message_id}, 
        message_order={self.message_order},
        created_at={self.created_at})>"""
from enum import Enum

class messageTypeEnum(str, Enum):
    user = 'user'
    llm = 'llm'
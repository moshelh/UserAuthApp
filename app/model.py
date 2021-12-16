from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Boolean
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(256))
    username = Column(String(256))
    password = Column(String(256))
    email = Column(String(256))
    disabled = Column(Boolean)

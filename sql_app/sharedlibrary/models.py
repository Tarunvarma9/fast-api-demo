from typing import Text
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TEXT

from sharedlibrary.database import Base


class User(Base):
    __tablename__ = "users_details"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(TEXT, unique=True, index=True)
    email = Column(TEXT, unique=True, index=True)
    password = Column(TEXT)


# from typing import Text
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# from sqlalchemy.sql.sqltypes import TEXT

from sharedlibrary.database import Base


class User(Base):
    __tablename__ = "user_detail"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    email = Column(String)
    password = Column(String)




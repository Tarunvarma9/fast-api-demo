from typing import List, Optional, Text

from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import TEXT,INTEGER



class UserBase(BaseModel):
    email: str


class User(UserBase):
    id: int
    user_name: str
    email: str
    password: str
    
    class Config:
        orm_mode = True
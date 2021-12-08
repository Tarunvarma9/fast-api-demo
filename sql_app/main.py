from typing import List
import jwt
from fastapi import Depends, FastAPI, HTTPException
from pydantic.utils import is_valid_field
from sqlalchemy import schema
from sqlalchemy.orm import Session, session
import shelve
from passlib.context import CryptContext
from sqlalchemy.sql.functions import current_user, user
from sharedlibrary import crud,models, schemas

from sharedlibrary.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

s = shelve.open("test", writeback = True)
s['auth'] = []        

pwd_context= CryptContext(schemas=["bcrypt"],deprecated='auto')


@app.get("/users_details/")
def read_users(db: Session = Depends(get_db)):
    # users = crud.get_users(db, skip=skip, limit=limit)
    usersDetails = db.query(models.User).all()
    return usersDetails


@app.get("/users_details/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



# @app.get("/login")
# def read_item(user_name:str, password:str,db: Session = Depends(get_db)):
#     users = crud.get_users(db)
#     us = ''
#     ps= ''
#     for i in users:
#         if(i.user_name == user_name):
#             us = i.user_name
#             ps = i.password
#     if user_name == us:
#         if str(ps) == password:
#             payload_data = {"user_name": user_name}
#             encoded_jwt = jwt.encode(payload=payload_data, key="secreat")
#             s['auth'].append(encoded_jwt)
#             return("login success", encoded_jwt)
#         else:
#             return("username and password not matched")

#     else:
#         return("login error")

@app.post('/signup')
def create_user(request:schemas.User,db: Session = Depends(get_db)):
    hashedPassword=pwd_context.hash(request.password)
    new_user=models.User(user_name=request.user_name, email=request.email,password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post('/login')
def login(request:schemas.Data,db:Session= Depends(get_db)):
    current_user=db.query(models.User).filter(models.User.user_name == request.user_name).first()
    is_valid=current_user.password==request.password
    if is_valid:
        return "user found"
    return "user not found"
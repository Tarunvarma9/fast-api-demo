from typing import List
import jwt
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import shelve
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


@app.get("/users_details/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users_details/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@app.get("/login")
def read_item(user_name:str, password:str,db: Session = Depends(get_db)):
    users = crud.get_users(db)
    us = ''
    ps= ''
    for i in users:
        if(i.user_name == user_name):
            us = i.user_name
            ps = i.password
    if user_name == us:
        if str(ps) == password:
            payload_data = {"user_name": user_name}
            encoded_jwt = jwt.encode(payload=payload_data, key="secreat")
            s['auth'].append(encoded_jwt)
            return("login success", encoded_jwt)
        else:
            return("username and password not matched")

    else:
        return("login error")
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
        
@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}
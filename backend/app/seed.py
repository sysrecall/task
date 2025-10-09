# seed database
from .database import get_session
from sqlmodel import Session, delete
from typing import Annotated
from fastapi import Depends
import requests as req
import json
from fastapi import APIRouter
from .movies.model import Movie

router = APIRouter(
    prefix="/seed", tags=["Seed"]
)

# load json data from disk or url
def get_data(path="data.json"):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def drop_table(session: Session):
    statement = delete(Movie)
    session.exec(statement=statement)
    session.commit()

@router.get("/")
def seed(session: Annotated[Session, Depends(get_session)]):
    drop_table(session)

    # get data from a file or the live link
    data = get_data()
    if not data:
        return {"message": "no data to add"}

    # seed table
    for d in data:
        session.add(Movie(**d))
    session.commit()

    return {"message": "data added"}
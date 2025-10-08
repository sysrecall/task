# seed database
from database import get_session
from sqlmodel import Session, delete
from typing import Annotated
from fastapi import Depends
import requests as req
import json
from fastapi import APIRouter
from posts.model import Post

router = APIRouter(
    prefix="/seed", tags=["Seed"]
)

# load json data from disk or url
def get_data(live=False, path="data.json"):
    if live:
        try:
            res = req.get("https://jsonplaceholder.typicode.com/posts")
            return res.json()
        except req.exceptions.RequestException as e:
            print(e)
            return

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def drop_table(session: Session):
    # drop table
    statement = delete(Post)
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
        session.add(Post(**d))
    session.commit()

    return {"message": "data added"}
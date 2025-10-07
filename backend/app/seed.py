# seed database
from database import get_session
from sqlmodel import Session
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

@router.get("/")
def seed(session: Annotated[Session, Depends(get_session)]):
    data = get_data()
    if not data:
        return {"message": "no data to add"}

    for d in data:
        session.add(Post(**d))
    session.commit()

    return {"message": "data added"}
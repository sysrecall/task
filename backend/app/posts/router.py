from fastapi import APIRouter 
from .schema import Post
from database import get_session
from sqlmodel import Session, select
from typing import Annotated, Sequence
from fastapi import Depends
from posts.model import Post

router = APIRouter(
    prefix="/posts"
)

@router.get("/", tags=["/"])
async def root(session: Annotated[Session, Depends(get_session)], 
               page: int = 1, size: int = 10) -> Sequence[Post]:

    statement = select(Post)    
    return session.exec(statement).all()

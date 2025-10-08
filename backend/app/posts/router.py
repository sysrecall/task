from fastapi import APIRouter, HTTPException
from .schemas.Post import Post
from .schemas.GetPosts import GetPostsSchema
from database import get_session
from sqlmodel import Session, select, desc, asc
from typing import Annotated, Sequence, Literal
from fastapi import Depends, Query
from posts.model import Post

router = APIRouter(
    prefix="/posts"
)

SORT_OPTIONS = {
    "userId": Post.userId,
    "id": Post.id,
}

ORDER_OPTIONS = {
    "desc": desc,
    "asc": asc
}

def get_posts(session: Session, query: Annotated[GetPostsSchema, Query()]):
    statement = select(Post)

    # filter by userId
    if query.userId != None:
        statement = statement.where(Post.userId == query.userId)

    # sort by given column and order
    if query.sort:
        if query.sort not in SORT_OPTIONS:
            raise HTTPException(status_code=400, detail="Invalid sort option!")

        if query.order not in ORDER_OPTIONS:
            raise HTTPException(status_code=400, detail="Invalid order option!")

        statement = statement.order_by(
            ORDER_OPTIONS[query.order](
                SORT_OPTIONS[query.sort]
            )
        )

    # apply size and limit of results
    offset = (query.page - 1) * query.size
    statement = statement.offset(offset).limit(query.size)  
    
    return session.exec(statement).all()


@router.get("/", tags=["/"])
async def root(
        session: Annotated[Session, Depends(get_session)], 
        query: Annotated[GetPostsSchema, Query()]
    ) -> Sequence[Post]:

    return get_posts(session, query)

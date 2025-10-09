from fastapi import APIRouter, HTTPException
from .schemas.Movie import Movie as MovieSchema
from .schemas.GetMovies import GetMoviesSchema 
from ..database import get_session
from sqlmodel import Session, select, desc, asc, column
from typing import Annotated, Sequence, Literal
from fastapi import Depends, Query
from .model import Movie as MovieModel
from ..decorators import cache

router = APIRouter(
    prefix="/movies"
)

SORT_OPTIONS = {
    "id": MovieModel.id,
    "title": MovieModel.title,
    "genre": MovieModel.genre,
    "released": MovieModel.released,
}

ORDER_OPTIONS = {
    "desc": desc,
    "asc": asc
}

@cache(expire_time=300, exclude_params=['session'])
def get_movies(session: Session, query: Annotated[GetMoviesSchema, Query()]):
    statement = select(MovieModel)

    # filter by genre
    if query.genre:
        statement = statement.where(column("genre").contains(query.genre))

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

    # apply offset and limit
    offset = (query.page - 1) * query.size
    statement = statement.offset(offset).limit(query.size)  
    
    return session.exec(statement).all()


@router.get("/", tags=["/"])
async def root(
        session: Annotated[Session, Depends(get_session)], 
        query: Annotated[GetMoviesSchema, Query()]
    ) -> Sequence[MovieSchema]:

    return await get_movies(session, query)

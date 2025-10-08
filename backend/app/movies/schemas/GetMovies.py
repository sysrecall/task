from pydantic import BaseModel
from typing import Literal

class GetMoviesSchema(BaseModel):
    sort: Literal["id", "title", "genre", "released"] | None = None
    order: Literal["desc", "asc"] = "desc"
    page: int = 1
    size: int = 10
    genre: str | None = None
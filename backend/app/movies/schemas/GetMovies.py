from pydantic import BaseModel
from typing import Literal

class GetMoviesSchema(BaseModel):
    sort: Literal["id", "title", "genre", "released"] | None = None
    order: Literal["desc", "asc"] = "asc"
    page: int = 1
    size: int = 10
    genre: str | None = None


    def __hash__(self):
        return hash((self.sort, self.order, self.page, self.size, self.genre))
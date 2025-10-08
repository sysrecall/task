from pydantic import BaseModel
from typing import Literal

class GetPostsSchema(BaseModel):
    sort: Literal["id", "userId"] | None = None
    order: Literal["desc", "asc"] = "desc"
    page: int = 1
    size: int = 10
    userId: int | None = None
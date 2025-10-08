from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str 
    genre: str
    released: int 
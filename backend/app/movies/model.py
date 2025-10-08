from sqlmodel import SQLModel, Field

class Movie(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str 
    genre: str
    released: int 
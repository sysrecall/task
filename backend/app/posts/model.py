from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):
    userId: int
    id: int = Field(primary_key=True)
    title: str
    body: str
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from movies.router import router as movie_router
from seed import router as seed_router 
from contextlib import asynccontextmanager
from database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()    
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(movie_router)
app.include_router(seed_router)

@app.get("/", tags=["Home"])
async def root():
    return {"message": "Hello, World!"}

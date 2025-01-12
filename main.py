from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routes import alunos, exercicios, treinos

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"msg": "Bem-vindo ao FastAPI!"}

app.include_router(alunos.router)
app.include_router(exercicios.router)
app.include_router(treinos.router)
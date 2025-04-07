from src.database import models as db_models
from src.database.database import engine
from src.game_of_life.game_of_life import GameOfLife
from src.utils.config import Config
from src.models import models as py_models
from typing import Union

from fastapi import FastAPI


gol = GameOfLife()

config = Config()
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/evolve")
async def evolve(request: py_models.EvolutionRequest):
    return await gol.check_evolution(request)

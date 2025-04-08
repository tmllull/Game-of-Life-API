from src.database import models as db_models
from src.config.database import engine
from src.game_of_life.game_of_life import GameOfLife
from src.config.config import Config
from src.models import models as py_models
from typing import Union
from src.auth import auth

from fastapi import FastAPI, Security


gol = GameOfLife()

config = Config()
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root(api_key: str = Security(auth.get_api_key)):
    return {"Hello": "World"}


@app.post("/evolve")
async def evolve(
    request: py_models.EvolutionRequest, api_key: str = Security(auth.get_api_key)
):
    msg, ecosystem, db_ecosystem = await gol.check_evolution(request)
    return {"message": msg, "ecosystem": ecosystem, "db_ecosystem": db_ecosystem}

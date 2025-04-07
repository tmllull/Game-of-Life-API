from pydantic import BaseModel


class EvolutionRequest(BaseModel):
    message: str
    user: str


class EvolutionResponse(BaseModel):
    message: str
    ecosystem: str
    # evolution: str = None  # Optional field for the evolution message
    # evolution_id: int
    # evolution_date: str
    # creator: str = None  # Optional field for the creator of the ecosystem
    # killer: str = None  # Optional field for the killer of the ecosystem

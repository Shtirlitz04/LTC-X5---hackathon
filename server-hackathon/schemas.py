from pydantic import BaseModel
from typing import List

class PredictRequest(BaseModel):
    input: str

class EntityResponse(BaseModel):
    start_index: int
    end_index: int
    entity: str

class HealthResponse(BaseModel):
    status: str
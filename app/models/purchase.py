from uuid import UUID
from pydantic import BaseModel
from typing import List

class Purchase(BaseModel):
    song_ids: List[UUID]
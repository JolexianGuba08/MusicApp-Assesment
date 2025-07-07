from datetime import datetime,timezone
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator

class SongBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    length: int = Field(..., gt=0, description="Length in seconds, must be positive")
    date_released: datetime
    price: float = Field(..., gt=0.0, le=999.99, description="Price must be a positive number")

    @validator("date_released")
    def validate_date(cls, v):
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc) 
        if v > datetime.now(timezone.utc):
            raise ValueError("Release date cannot be in the future")
        return v

class SongCreate(SongBase):
    pass


class Song(SongBase):
    id: Optional[UUID] = None

class SongUpdate(SongBase):
    title: Optional[str] = None
    length: Optional[int] = None
    date_released: Optional[datetime] = None
    price: Optional[float] = None

from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from app.models.song import Song

class PlaylistBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Playlist name must be between 1 and 100 characters")
    created_at: datetime

class Playlist(PlaylistBase):
    id: Optional[UUID] = None
    song_count : int

class CreatePlaylist(PlaylistBase):
    name: str
    song_ids: List[UUID]
    created_at: Optional[datetime] = None

class PlaylistWithSongs(BaseModel):
    id: Optional[UUID] = None
    name: str
    songs: List[Song] = []
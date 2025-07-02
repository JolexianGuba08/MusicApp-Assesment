from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4

class PlaylistSongLink(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    playlist_id: UUID = Field(foreign_key="playlist.id")
    song_id: UUID = Field(foreign_key="song.id")


class Song(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    title: str
    length: int
    date_released: datetime
    price: float
    playlists: List["Playlist"] = Relationship(
        back_populates="songs", link_model=PlaylistSongLink
    )


class Playlist(SQLModel, table=True):

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    songs: List[Song] = Relationship(
        back_populates="playlists", link_model=PlaylistSongLink
    )

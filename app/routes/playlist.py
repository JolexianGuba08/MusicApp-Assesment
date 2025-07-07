from datetime import datetime
import random
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException,status
from app.models.playlist import CreatePlaylist, Playlist, PlaylistWithSongs
from app.database import supabase

router = APIRouter()

@router.post("/", response_model=PlaylistWithSongs, status_code=status.HTTP_201_CREATED)
async def create_playlist(playlist: CreatePlaylist):
    try:
  
        response = supabase.table("playlist").insert({
            "name": playlist.name,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        if not response.data or not response.data[0]:
            raise HTTPException(status_code=404, detail="Error creating playlist")

        playlist_data = response.data[0]
        playlist_id = playlist_data["id"]

        #Prevent duplicate song links
        for song_id in playlist.song_ids:
            existing_link = supabase.table("playlistsonglink")\
                .select("*")\
                .eq("playlist_id", str(playlist_id))\
                .eq("song_id", str(song_id))\
                .execute()

            if existing_link.data:
                raise HTTPException(
                    status_code=409,
                    detail=f"Song {song_id} is already in the playlist."
                )

            supabase.table("playlistsonglink").insert({
                "playlist_id": str(playlist_id),
                "song_id": str(song_id)
            }).execute()

        if playlist.song_ids:
            songs_response = supabase.table("song")\
                .select("*")\
                .in_("id", playlist.song_ids)\
                .execute()
            songs = songs_response.data
        else:
            songs = []

        return {
            "id": playlist_id,
            "name": playlist_data["name"],
            "songs": songs
        }

    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/shuffle/{playlist_id}", response_model=PlaylistWithSongs, status_code=status.HTTP_200_OK)
async def shuffle_playlist(playlist_id: UUID):
    try:
    
        playlist_response = supabase.table("playlist").select("*").eq("id", playlist_id).execute()
        
        if not playlist_response.data or len(playlist_response.data) == 0:
            raise HTTPException(status_code=404, detail="Playlist not found")
        playlist = playlist_response.data[0]

        link_response = supabase.table("playlistsonglink").select("song_id").eq("playlist_id", playlist_id).execute()
        song_ids = [link["song_id"] for link in link_response.data]

        if not song_ids:
            songs = []
        else:
            songs_response = supabase.table("song").select("*").in_("id", song_ids).execute()
            songs = songs_response.data
            random.shuffle(songs)

        print("songs:",songs)
        return {
            "message":"Song shuffled successfully",
            "name": playlist["name"],
            "songs": songs
        }
    
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")



### ADDITIONALS ###
# GET ALL PLAYLIST
@router.get("/", response_model=List[Playlist], status_code=status.HTTP_200_OK)
async def get_all_playlists():
    try:
        playlist_response = supabase.table("playlist").select("*").execute()
        if not playlist_response.data:
            raise HTTPException(status_code=404, detail="No playlists found yet.")

        playlists_with_counts = []

        for playlist in playlist_response.data:
            link_response = supabase.table("playlistsonglink").select("song_id").eq("playlist_id", playlist["id"]).execute()
            song_count = len(link_response.data) if link_response.data else 0

            playlists_with_counts.append({
                "id": playlist["id"],
                "name": playlist["name"],
                "created_at": playlist["created_at"],
                "song_count": song_count
            })

        return playlists_with_counts

    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# GET SPECIFIC PLAYLIST
@router.get("/{playlist_id}", response_model=PlaylistWithSongs, status_code=status.HTTP_200_OK)
async def get_playlist_with_songs(playlist_id: UUID):
    try:
        playlist_response = supabase.table("playlist").select("*").eq("id", playlist_id).execute()
        if not playlist_response.data or len(playlist_response.data) == 0:
            raise HTTPException(status_code=404, detail="Playlist not found")
        
        playlist = playlist_response.data[0]


        link_response = supabase.table("playlistsonglink").select("song_id").eq("playlist_id", playlist_id).execute()
        song_ids = [link["song_id"] for link in link_response.data]

        if not song_ids:
            songs = []
        else:
            songs_response = supabase.table("song").select("*").in_("id", song_ids).execute()
            songs = songs_response.data

        return {
            "id": playlist["id"],
            "name": playlist["name"],
            "songs": songs 
        }

    except HTTPException as httpex:
        print(httpex)
        raise httpex
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


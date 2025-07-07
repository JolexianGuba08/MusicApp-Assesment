from typing import List
from fastapi import APIRouter, HTTPException, status, Request
from app.models.song import Song, SongCreate, SongUpdate
from app.services.payment import process_payment
from app.database import supabase
from uuid import UUID
router = APIRouter()

@router.get("/", response_model=List[Song],status_code=status.HTTP_200_OK)
async def get_all_songs():
    try:
        response = supabase.table("song").select("*").execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="No songs found")
        return response.data
    
    except HTTPException as http_ex:
        raise http_ex
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
   

@router.post("/", response_model=Song, status_code=status.HTTP_201_CREATED)
async def create_song(song: SongCreate):
    try:
        data = song.dict()
        data["date_released"] = data["date_released"].isoformat()

      
        check_response = supabase.table("song")\
            .select("*")\
            .eq("title", data["title"])\
            .eq("length", data["length"])\
            .eq("date_released", data["date_released"])\
            .execute()

        if check_response.data:
            raise HTTPException(
                status_code=409,
                detail="Song already exists with the same title, length, and release date."
            )

        response = supabase.table("song").insert(data).execute()

        if not response.data or not response.data[0]:
            raise HTTPException(status_code=400, detail="Error creating song")

        return response.data[0]

    except HTTPException as http_ex:
        print(http_ex)
        raise http_ex
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{song_id}", response_model=Song,status_code=status.HTTP_200_OK)
async def get_song(song_id: UUID):
    try:
        response = supabase.table("song").select("*").eq("id", song_id).execute()
        print(response)
        if not response.data :
            raise HTTPException(status_code=404, detail="Song not found")
        
        return response.data[0]
    
    except HTTPException as http_ex:
        raise http_ex
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.put("/{song_id}", response_model=Song, status_code=status.HTTP_200_OK)
async def update_song(song_id: UUID, song: SongUpdate):
    try:
        # to exclude unprovided fields
        data = song.dict(exclude_unset=True)
        response = supabase.table("song").update(data).eq("id", song_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Song not found") 
        return response.data[0]
    
    except HTTPException as http_ex:
        raise http_ex
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{song_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(song_id: UUID):
    try:
        response = supabase.table("song").delete().eq("id", song_id).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Song not found") 
        return 
    
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

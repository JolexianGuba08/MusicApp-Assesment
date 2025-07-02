
from fastapi import APIRouter, HTTPException, status, Request
from typing import List
from app.services.payment import process_payment
from app.database import supabase
from app.models.purchase import Purchase

router = APIRouter()

@router.post("/",status_code=status.HTTP_201_CREATED)
async def purchase_songs(request:Purchase):
    total_price = 0
    try:
        for song_id in request.song_ids:
            song_response = supabase.table("song").select("price").eq("id", song_id).execute()
            if not song_response.data:
                raise HTTPException(status_code=404, detail=f"Song with id {song_id} not found")
            total_price += song_response.data[0]['price']

        payment_response = process_payment(total_price)
        return {"message": payment_response}
    
    except HTTPException as httpex:
        raise httpex
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

   


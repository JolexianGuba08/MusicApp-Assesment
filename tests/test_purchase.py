from datetime import datetime, timezone
import pytest
from uuid import uuid4
from unittest.mock import patch, MagicMock


@pytest.mark.asyncio

async def test_purchase_songs_success(client):
    song_id1 = str(uuid4())
    song_id2 = str(uuid4())
    
    print(f"DEBUG: Test song IDs - song_id1: {song_id1}, song_id2: {song_id2}")
    with patch("app.routes.purchase.supabase") as mock_supabase:
        mock_response_1 = MagicMock()
        mock_response_1.data = [{"price": 10.0}]
        
        mock_response_2 = MagicMock()
        mock_response_2.data = [{"price": 15.0}]


        mock_table = MagicMock()
        mock_select = MagicMock()
        mock_eq = MagicMock()
        
        mock_supabase.table.return_value = mock_table
        mock_table.select.return_value = mock_select
        mock_select.eq.return_value = mock_eq
        

        mock_eq.execute.side_effect = [mock_response_1, mock_response_2]
        
        print(f"DEBUG: Mock setup complete")
        with patch("app.routes.purchase.process_payment") as mock_payment:
            mock_payment.return_value = "Payment successful"
            
            print(f"DEBUG: Making request")
            response = await client.post(
                "/api/purchase/",
                json={"song_ids": [song_id1, song_id2]}
            )
            
            assert response.status_code == 201
            assert response.json() == {"message": "Payment successful"}
            mock_payment.assert_called_once_with(25.0)
  
@pytest.mark.asyncio
async def test_purchase_song_not_found(client, mock_supabase):
    song_id = str(uuid4())

    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

    payload = {
        "song_ids": [song_id]
    }

    response = await client.post("/api/purchase/", json=payload)

    assert response.status_code == 404
    assert response.json()["detail"] == f"Song with id {song_id} not found"

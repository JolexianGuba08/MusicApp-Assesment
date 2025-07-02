import pytest
from uuid import uuid4
from datetime import datetime, timezone
from unittest.mock import MagicMock

sample_song = {
    "title": "Test Song",
    "length": 180,
    "date_released": datetime.now(timezone.utc).isoformat(),
    "price": 9.99
}

@pytest.mark.asyncio
async def test_get_all_songs(client, mock_supabase):
    mock_supabase.execute.return_value.data = [sample_song]
    response = await client.get("/api/song/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_all_songs_empty(client, mock_supabase):
    mock_supabase.execute.return_value.data = []
    response = await client.get("/api/song/")
    assert response.status_code == 404
    assert response.json()["detail"] == "No songs found"

@pytest.mark.asyncio
async def test_create_song(client, mock_supabase):
    mock_supabase.execute.side_effect = [
        MagicMock(data=[]),            
        MagicMock(data=[sample_song]) 
    ]
    response = await client.post("/api/song/", json=sample_song)

    assert response.status_code == 201
    assert response.json()["title"] == "Test Song"

    
@pytest.mark.asyncio
async def test_create_song_conflict(client, mock_supabase):
    mock_supabase.execute.return_value.data = [sample_song]
    response = await client.post("/api/song/", json=sample_song)
    assert response.status_code == 409
    assert response.json()["detail"] == "Song already exists with the same title, length, and release date."

@pytest.mark.asyncio
async def test_create_song_invalid_data(client):
    invalid_song = sample_song.copy()
    invalid_song["price"] = "free"   

    response = await client.post("/api/song/", json=invalid_song)
    assert response.status_code == 422  

@pytest.mark.asyncio
async def test_get_song_by_id(client, mock_supabase):
    song_id = uuid4()
    current_datetime = datetime.now(timezone.utc)

    db_response = {
        "id": str(song_id), 
        "title": "Test Song",
        "length": 180,
        "date_released": current_datetime.isoformat(), 
        "price": 9.99
    }
    
    mock_supabase.execute.return_value.data = [db_response]
    
    response = await client.get(f"/api/song/{song_id}")
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == str(song_id)
    assert response_data["title"] == "Test Song"
    assert response_data["length"] == 180
    assert datetime.fromisoformat(response_data["date_released"]) == current_datetime

@pytest.mark.asyncio
async def test_get_song_by_id_not_found(client, mock_supabase):
    mock_supabase.execute.return_value.data = []
    song_id = str(uuid4())
    response = await client.get(f"/api/song/{song_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Song not found"

@pytest.mark.asyncio
async def test_update_song(client, mock_supabase):
    song_id = str(uuid4())
    updated_data = {**sample_song, "title": "Updated Title"}
    mock_supabase.execute.return_value.data = [updated_data]
    response = await client.put(f"/api/song/{song_id}", json={"title": "Updated Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

@pytest.mark.asyncio
async def test_update_song_not_found(client, mock_supabase):
    song_id = str(uuid4())
    mock_supabase.execute.return_value.data = []
    response = await client.put(f"/api/song/{song_id}", json={"title": "New Title"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Song not found"

@pytest.mark.asyncio
async def test_delete_song(client, mock_supabase):
    song_id = str(uuid4())
    mock_supabase.execute.return_value.data = [{"id": song_id}]
    response = await client.delete(f"/api/song/{song_id}")
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_delete_song_not_found(client, mock_supabase):
    song_id = str(uuid4())
    mock_supabase.execute.return_value.data = []
    response = await client.delete(f"/api/song/{song_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Song not found"

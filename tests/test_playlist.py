import pytest
from uuid import uuid4
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

@pytest.mark.asyncio
async def test_create_playlist(client):
    playlist_id = str(uuid4())
    now = datetime.now(timezone.utc).isoformat()
    song_id_1 = str(uuid4())
    song_id_2 = str(uuid4())

    with patch("app.routes.playlist.supabase") as mock_supabase:

        playlist_insert_response = MagicMock()
        playlist_insert_response.data = [{
            "id": playlist_id,
            "name": "Study Vibes",
            "created_at": now
        }]

    
        duplicate_check_response = MagicMock()
        duplicate_check_response.data = []

        song_link_insert_response = MagicMock()
        song_link_insert_response.data = [{"playlist_id": playlist_id, "song_id": song_id_1}]

        songs_fetch_response = MagicMock()
        songs_fetch_response.data = [
            {
                "id": song_id_1,
                "title": "Focus",
                "length": 180,
                "date_released": now,
                "price": 1.99
            },
            {
                "id": song_id_2,
                "title": "Concentration",
                "length": 200,
                "date_released": now,
                "price": 2.99
            }
        ]

      
        def mock_table_calls(table_name):
            if table_name == "playlist":
                mock_table = MagicMock()
                mock_table.insert.return_value.execute.return_value = playlist_insert_response
                return mock_table
            elif table_name == "playlistsonglink":
                mock_table = MagicMock()
               
                mock_table.select.return_value.eq.return_value.eq.return_value.execute.return_value = duplicate_check_response
                 
                mock_table.insert.return_value.execute.return_value = song_link_insert_response
                return mock_table
            elif table_name == "song":
                mock_table = MagicMock()
                mock_table.select.return_value.in_.return_value.execute.return_value = songs_fetch_response
                return mock_table

        mock_supabase.table.side_effect = mock_table_calls

        payload = {
            "name": "Study Vibes",
            "song_ids": [song_id_1, song_id_2]
        }

        print(f"DEBUG: Making playlist request")
        response = await client.post("/api/playlist/", json=payload)
        
        print(f"DEBUG: Response status: {response.status_code}")
        if response.status_code != 201:
            print(f"DEBUG: Response body: {response.json()}")

        assert response.status_code == 201
        data = response.json()

        assert data["name"] == "Study Vibes"
        assert isinstance(data["songs"], list)
        assert len(data["songs"]) == 2
        assert data["songs"][0]["id"] in [song_id_1, song_id_2]

@pytest.mark.asyncio
async def test_shuffle_playlist(client, mock_supabase):
    playlist_id = str(uuid4())
    playlist_data = {"id": playlist_id, "name": "Roadtrip"}
    song_ids = [str(uuid4()), str(uuid4())]
    songs_data = [
        {"id": song_ids[0], "title": "A", "length": 100, "date_released": datetime.now().isoformat(), "price": 2.0},
        {"id": song_ids[1], "title": "B", "length": 120, "date_released": datetime.now().isoformat(), "price": 3.0}
    ]

    mock_supabase.execute.side_effect = [
        MagicMock(data=[playlist_data]),         # playlist lookup
        MagicMock(data=[{"song_id": sid} for sid in song_ids]),  # link lookup
        MagicMock(data=songs_data)              # songs lookup
    ]

    response = await client.get(f"/api/playlist/shuffle/{playlist_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Roadtrip"
    assert isinstance(response.json()["songs"], list)

@pytest.mark.asyncio
async def test_get_all_playlists(client, mock_supabase):
    playlists = [
        {"id": str(uuid4()), "name": "Mix 1", "created_at": datetime.now().isoformat()},
        {"id": str(uuid4()), "name": "Mix 2", "created_at": datetime.now().isoformat()}
    ]
    mock_supabase.execute.side_effect = [
        MagicMock(data=playlists),   # all playlists
        MagicMock(data=[{"song_id": str(uuid4())}]),  # song link for 1
        MagicMock(data=[])  # song link for 2
    ]

    response = await client.get("/api/playlist/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert "song_count" in response.json()[0]

@pytest.mark.asyncio
async def test_get_playlist_with_songs(client, mock_supabase):
    playlist_id = str(uuid4())
    playlist = {"id": playlist_id, "name": "Gym Mix", "created_at": datetime.now().isoformat()}
    song_ids = [str(uuid4())]
    songs = [{
        "id": song_ids[0], "title": "Push Hard", "length": 180,
        "date_released": datetime.now().isoformat(), "price": 1.99
    }]

    mock_supabase.execute.side_effect = [
        MagicMock(data=[playlist]),   # playlist
        MagicMock(data=[{"song_id": sid} for sid in song_ids]),  # links
        MagicMock(data=songs)  # songs
    ]

    response = await client.get(f"/api/playlist/{playlist_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Gym Mix"
    assert isinstance(response.json()["songs"], list)

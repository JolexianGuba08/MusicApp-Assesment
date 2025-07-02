Here’s your exact README content reformatted for better **presentation and visual clarity**, while keeping your wording **unchanged**:

---

# 🎵 Music App API

The Music App API is a modern backend platform for a music streaming service built using **FastAPI**. It provides functionalities for song management, playlist creation, and secure payment processing. The API is designed to be efficient and user-friendly, allowing users to easily manage their music library and playlists.

---

## ⚙️ Tech Stack

| Category               | Technologies                                |
| ---------------------- | ------------------------------------------- |
| **Backend Framework**  | FastAPI – A modern, fast web framework      |
| **Language**           | Python 3.8+                                 |
| **ASGI Server**        | Uvicorn                                     |
| **Database & Storage** | Supabase (PostgreSQL)                       |
| **Validation**         | Pydantic, UUID                              |
| **Testing**            | `pytest`, `pytest-asyncio`, `unittest.mock` |
| **Dev Tools**          | Virtualenv, Git                             |

---

## 📡 API Endpoints

### 🎵 Songs

* `GET /api/song/` – Retrieve all songs
* `POST /api/song/` – Create a new song
* `GET /api/song/{song_id}` – Retrieve a song by its ID
* `PUT /api/song/{song_id}` – Update an existing song
* `DELETE /api/song/{song_id}` – Delete a song

### 📁 Playlists

* `POST /api/playlist/` – Create a new playlist
* `GET /api/playlist/shuffle/{playlist_id}` – Shuffle songs in a playlist
* `GET /api/playlist/` – Retrieve all playlists
* `GET /api/playlist/{playlist_id}` – Retrieve a playlist with its songs

### 💳 Purchases

* `POST /api/purchase/` – Purchase songs

### 📖 Docs

* `GET /openapi.json` – OpenAPI schema
* `GET /docs` – Swagger UI
* `GET /docs/oauth2-redirect` – OAuth2 redirect
* `GET /redoc` – ReDoc docs

---

## 🚀 Running the Application

```bash
uvicorn app.main:app
```

---

## 🧪 Testing

* Run all tests

  ```bash
  pytest
  ```

* Run tests with coverage

  ```bash
  pytest --cov=app
  ```

* Run a specific test file

  ```bash
  pytest tests/test_purchase.py
  ```

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---


# 🎵 Music App API

A modern music streaming platform backend built with FastAPI, featuring song management, playlist creation, and secure payment processing.

## ✨ Features

- **Song Management**: Upload, update, and manage your music library
- **Playlist Creation**: Create and manage custom playlists
- **Purchase System**: Simple song purchasing with payment processing
- **Testing Suite**: Comprehensive unit tests with pytest

## 🛠️ Tech Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework for building APIs with Python
- **Python 3.8+** - Programming language
- **Uvicorn** - ASGI server for running the application

### Database & Storage
- **Supabase** - Backend-as-a-Service with PostgreSQL database
- **PostgreSQL** - Relational database for data persistence

### Data Validation & Serialization
- **Pydantic** - Data validation using Python type annotations
- **UUID** - Unique identifiers for database records

### Testing
- **pytest** - Testing framework
- **pytest-asyncio** - Async testing support
- **unittest.mock** - Mock objects for testing

### Development Tools
- **Python Virtual Environment** - Dependency isolation
- **Git** - Version control

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Supabase account and project

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/music-app.git
   cd music-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_purchase.py
```

## 📋 API Endpoints

### Songs
- `POST /api/songs/` - Create a new song
- `GET /api/songs/{id}` - Get song by ID
- `PUT /api/songs/{id}` - Update song
- `DELETE /api/songs/{id}` - Delete song

### Playlists
- `POST /api/playlist/` - Create a new playlist
- `GET /api/playlist/{id}` - Get playlist by ID
- `PUT /api/playlist/{id}` - Update playlist
- `DELETE /api/playlist/{id}` - Delete playlist

### Purchases
- `POST /api/purchase/` - Purchase songs

## 🔧 Environment Variables

Create a `.env` file in the root directory:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- Supabase for the backend infrastructure
- The Python community for excellent tooling

---

Built with ❤️ using FastAPI and Python

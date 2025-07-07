from fastapi import FastAPI
from app.routes import song, playlist, purchase
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(song.router, prefix="/api/song")
app.include_router(playlist.router, prefix="/api/playlist")
app.include_router(purchase.router, prefix="/api/purchase")
print(app.routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Music API"}

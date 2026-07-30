import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://movie-companion-psi.vercel.app","http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat.router, prefix="/api")

@app.get("/")
def greet():
    return{"status":"ok", "message":"Movie Companion is hereee"}
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
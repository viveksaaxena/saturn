from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, notes

app = FastAPI(title="Notes App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers exactly as defined
app.include_router(auth.router)        # prefix already inside auth.py
app.include_router(notes.router)       # prefix inside notes.py

@app.get("/")
def read_root():
    return {"message": "Notes App API is running!"}

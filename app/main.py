from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import your routes here (example)
from . import routes  # You will need to adapt your routes.py for FastAPI

# Example health check endpoint
@app.get("/api/health")
def health():
    return {"status": "healthy"}
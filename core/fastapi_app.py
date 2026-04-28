import os
import django
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 1. BRIDGE TO DJANGO
# This allows FastAPI to access your db.sqlite3 through Django's models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecodrop_api.settings')
django.setup()

try:
    from core.models import Bin 
except ImportError:
    # This is a fallback just in case the folder structure is tricky
    from models import Bin

app = FastAPI(title="EcoDrop API - Powered by FastAPI")

# 2. CORS CONFIGURATION
# This is the "Key" that lets your React frontend talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For the presentation, '*' allows any frontend to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. ENDPOINTS
@app.get("/api/v1/health")
async def health_check():
    return {"status": "FastAPI is running", "database": "Connected to Django"}

@app.get("/api/v1/bins")
async def get_bins():
    """
    Fetches all trash bin locations from the Django database 
    and serves them as high-speed JSON.
    """
    # .values() converts Django objects into a list of dictionaries (JSON)
    bins_data = list(Bin.objects.all().values())
    return bins_data

# 4. SWAGGER DOCS HACK
# Tell your instructor that FastAPI automatically builds 
# documentation at /docs or /redoc
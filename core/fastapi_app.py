import os
import django
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware  # NEW: Added WSGI Middleware
from django.core.wsgi import get_wsgi_application   # NEW: Added Django app fetcher

# 1. BRIDGE TO DJANGO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecodrop_api.settings')
django.setup()

# NEW: Get the Django app immediately after setup
django_app = get_wsgi_application()


from core.models import SmartBin # Note: Ensure your model is actually named 'Bin' and not 'SmartBin'

app = FastAPI(title="EcoDrop API - Powered by FastAPI")

# 2. CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. FASTAPI ENDPOINTS
@app.get("/api/v1/health")
async def health_check():
    return {"status": "FastAPI is running", "database": "Connected to Django"}

@app.get("/api/v1/bins")
def get_bins():
    bins_data = list(SmartBin.objects.all().values())
    return bins_data

# 4. DJANGO FALLBACK (CRITICAL FIX)
# This catches everything that isn't a FastAPI route (like /api/login/) 
# and sends it to Django DRF
app.mount("/", WSGIMiddleware(django_app))
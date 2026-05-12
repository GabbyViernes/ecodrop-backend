import os
import django
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware  # From local: Added WSGI Middleware
from django.core.wsgi import get_wsgi_application   # From local: Added Django app fetcher
from pydantic import BaseModel                      # From remote
from typing import Optional                         # From remote
from asgiref.sync import sync_to_async              # From remote

# 1. BRIDGE TO DJANGO
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecodrop_api.settings')
django.setup()

# NEW: Get the Django app immediately after setup
django_app = get_wsgi_application()

# Import Django models
from core.models import SmartBin, UserProfile

app = FastAPI(title="EcoDrop API - Powered by FastAPI")

# 2. CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. PYDANTIC SCHEMA
class UserProfileUpdate(BaseModel):
    display_name: Optional[str] = None
    phone_number: Optional[str] = None


# 4. FASTAPI ENDPOINTS
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "FastAPI is running",
        "database": "Connected to Django"
    }

@app.get("/api/v1/bins")
async def get_bins():
    get_bins_sync = sync_to_async(lambda: list(SmartBin.objects.all().values()))
    bins_data = await get_bins_sync()
    return bins_data

# ── Task 2: User Profile ──────────────────────────────────────────────────────

@app.get("/api/v1/profiles/{user_id}")
async def get_profile(user_id: int):
    def fetch_profile():
        try:
            return UserProfile.objects.select_related('user').get(user__id=user_id)
        except UserProfile.DoesNotExist:
            return None

    profile = await sync_to_async(fetch_profile)()

    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "user_id": profile.user.id,
        "username": profile.user.username,
        "display_name": profile.display_name,
        "phone_number": profile.phone_number,
        "total_eco_points": profile.total_eco_points,
        "message": f"Welcome back, {profile.display_name or profile.user.username}! You have {profile.total_eco_points} points."
    }


@app.patch("/api/v1/profiles/{user_id}")
async def update_profile(user_id: int, data: UserProfileUpdate):
    def do_update():
        try:
            profile = UserProfile.objects.get(user__id=user_id)
            if data.display_name is not None:
                profile.display_name = data.display_name
            if data.phone_number is not None:
                profile.phone_number = data.phone_number
            profile.save()
            return profile
        except UserProfile.DoesNotExist:
            return None

    profile = await sync_to_async(do_update)()

    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "message": "Profile updated successfully",
        "display_name": profile.display_name,
        "phone_number": profile.phone_number,
    }


# 5. DJANGO FALLBACK (CRITICAL FIX)
# catches everything that isn't a FastAPI route (like /api/login/) 
# and sends it to Django DRF
app.mount("/", WSGIMiddleware(django_app))
import os
import datetime
import decimal
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY: str = os.environ.get("SUPABASE_ANON_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Import the new, unified get_current_user function
from app.auth import get_current_user

# Define API router
router = APIRouter(prefix="/parking", tags=["Parking Management"])

# Pydantic models for request/response validation
class ParkingSlotCreate(BaseModel):
    slot_name: str
    zone: str
    pricing_rate: float

class ReservationRequest(BaseModel):
    slot_id: str
    duration_hours: int

# --- API ENDPOINTS ---

# 1. Get all available parking slots
@router.get("/slots")
async def get_all_slots():
    """Retrieve all available parking slots."""
    try:
        response = supabase.from_('parking_slots').select('*').eq('status', 'available').execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Create a new parking slot (requires a valid JWT token)
@router.post("/slots", status_code=status.HTTP_201_CREATED)
async def create_slot(slot: ParkingSlotCreate, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Creates a new parking slot in the system."""
    try:
        response = supabase.from_('parking_slots').insert(slot.model_dump()).execute()
        return {"message": "Slot created successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 3. Reserve a parking slot (requires a valid JWT token)
@router.post("/reserve", status_code=status.HTTP_201_CREATED)
async def reserve_slot(reservation: ReservationRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Reserves an available parking slot for a user.
    """
    user_id = current_user.get('id')
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token.")

    # 1. Check if the slot is available
    slot_response = supabase.from_('parking_slots').select('*').eq('id', reservation.slot_id).execute()
    if not slot_response.data or slot_response.data[0]['status'] != 'available':
        raise HTTPException(status_code=400, detail="Slot not available or does not exist.")

    slot_data = slot_response.data[0]

    # 2. Calculate the cost and times
    start_time = datetime.datetime.now(datetime.timezone.utc)
    duration = datetime.timedelta(hours=reservation.duration_hours)
    end_time = start_time + duration
    
    total_cost = decimal.Decimal(slot_data['pricing_rate']) * decimal.Decimal(reservation.duration_hours)

    # 3. Create the reservation record and update slot status
    try:
        # Update the slot status to 'reserved' first
        supabase.from_('parking_slots').update({'status': 'reserved'}).eq('id', reservation.slot_id).execute()
        
        # Insert the new reservation record
        reservation_record = {
            "user_id": user_id,
            "slot_id": reservation.slot_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "total_cost": float(total_cost)
        }
        
        res_response = supabase.from_('reservations').insert(reservation_record).execute()
        
        return {
            "message": "Slot reserved successfully",
            "reservation_id": res_response.data[0]['id'],
            "total_cost": float(total_cost)
        }
    except Exception as e:
        # If anything fails, revert the slot status and raise an error
        supabase.from_('parking_slots').update({'status': 'available'}).eq('id', reservation.slot_id).execute()
        raise HTTPException(status_code=500, detail=f"Reservation failed: {e}")

# 4. View a user's own reservations
@router.get("/my-reservations")
async def get_my_reservations(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Retrieves all reservations for the currently authenticated user."""
    user_id = current_user.get('id')
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token.")
    
    try:
        response = supabase.from_('reservations').select('*').eq('user_id', user_id).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
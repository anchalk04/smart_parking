import os
import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()
SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY: str = os.environ.get("SUPABASE_ANON_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Define API router
router = APIRouter(tags=["Authentication"])

# --- Security Schemes for Swagger UI ---
# This scheme is for the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# This is the new, simpler scheme for protected endpoints
bearer_scheme = HTTPBearer()

# Pydantic models for request bodies
class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# --------------------
# Core Authentication Functions
# --------------------

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=2)):
    """Creates a new JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """Decodes and validates the JWT token to get the current user's ID."""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"id": user_id}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


# --------------------
# API Endpoints
# --------------------

@router.post("/register")
def register_user(request: RegisterRequest):
    """Registers a new user in Supabase Authentication."""
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password
        })
        if response.user:
            return {"message": "User registered successfully", "user_id": response.user.id}
        else:
            raise HTTPException(status_code=400, detail=response.message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login_user(request: LoginRequest):
    """Authenticates a user and returns a JWT token."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        if response.user:
            access_token = create_access_token({"user_id": response.user.id})
            return {"token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=400, detail=response.message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
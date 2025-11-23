from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from database import supabase

router = APIRouter(prefix="/api", tags=["Authentication"])  # changed prefix

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup(user: SignupRequest):
    try:
        existing = supabase.table("users").select("*").eq("email", user.email).execute()
        
        if existing.data:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        result = supabase.table("users").insert({
            "email": user.email,
            "password": user.password
        }).execute()
        
        return {"message": "User created successfully", "user_id": result.data[0]["id"]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login(user: LoginRequest):
    try:
        result = supabase.table("users").select("*").eq("email", user.email).eq("password", user.password).execute()
        
        if not result.data:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user_data = result.data[0]
        
        return {
            "message": "Login successful",
            "user_id": user_data["id"],
            "email": user_data["email"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

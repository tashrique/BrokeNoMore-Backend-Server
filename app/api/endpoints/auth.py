from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
import os

from app.api.deps import get_current_active_user, get_current_user
from app.core.config import settings
from app.db import get_db
from app.db.models import User
from app.models.user import Token, User as UserSchema
from app.services.auth import get_google_auth_url, authenticate_user

router = APIRouter()

@router.get("/login")
async def login_google():
    """
    Get Google OAuth login URL
    """
    return {"login_url": get_google_auth_url()}

@router.get("/callback")
async def auth_callback(code: str, response: Response, db: Session = Depends(get_db)):
    """
    Handle Google OAuth callback
    """
    try:
        token = authenticate_user(db, code)
        
        # Set cookie for frontend
        response.set_cookie(
            key="access_token",
            value=token.access_token,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 7,  # 7 days
            path="/"
        )
        
        # Redirect to frontend after successful login
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        return RedirectResponse(url=f"{frontend_url}/dashboard")
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        # Log the error for debugging
        print(f"OAuth callback error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )

@router.post("/logout")
async def logout(response: Response, current_user: User = Depends(get_current_active_user)):
    """
    Logout user by clearing the cookie
    """
    response.delete_cookie(key="access_token")
    return {"message": "Successfully logged out"}

@router.get("/profile", response_model=UserSchema)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    """
    Get current user profile
    """
    return current_user 
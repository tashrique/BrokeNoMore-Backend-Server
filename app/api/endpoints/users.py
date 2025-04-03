from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Optional
from app.db.supabase_client import get_supabase_client

router = APIRouter()


async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Verify the JWT token and return the user information.
    This can be used as a dependency for protected routes.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.replace("Bearer ", "")

    try:
        supabase = get_supabase_client()
        user_response = supabase.auth.get_user(token)

        if not user_response or not hasattr(user_response, 'user'):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or user not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_response.user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me")
async def get_user_info(current_user=Depends(get_current_user)):
    """
    Returns information about the currently authenticated user.
    This endpoint requires authentication.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "user_metadata": current_user.user_metadata,
        "app_metadata": current_user.app_metadata,
        "created_at": current_user.created_at,
    }

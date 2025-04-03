from fastapi import APIRouter, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.db.supabase_client import get_supabase_client


router = APIRouter()


@router.get('/login')
async def login_google():
    """
    Initiates the Google OAuth flow.

    The frontend should call this endpoint to start the login process.
    It will redirect to Google's login page, and after successful authentication,
    Google will redirect back to the Supabase auth callback URL, which will
    then redirect to your frontend with the tokens in the URL fragment.
    """
    try:
        supabase = get_supabase_client()

        # Initiate OAuth flow with Google
        auth_response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": settings.GOOGLE_REDIRECT_URI
            }
        })

        if not auth_response or not hasattr(auth_response, 'url'):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to initiate Google OAuth flow"
            )

        # Redirect to Google's consent page
        return RedirectResponse(url=auth_response.url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initiating Google OAuth flow: {str(e)}"
        )

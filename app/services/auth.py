import requests
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import UserCreate, Token
from app.services.user import get_or_create_user

def get_google_provider_cfg() -> Dict[str, Any]:
    """
    Get Google's provider configuration
    """
    try:
        return requests.get(settings.GOOGLE_DISCOVERY_URL).json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get Google provider configuration: {str(e)}"
        )

def get_google_auth_url() -> str:
    """
    Get Google authorization URL
    """
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    # Construct the request for Google login
    request_uri = f"{authorization_endpoint}?response_type=code&client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.OAUTH_REDIRECT_URI}&scope=openid email profile"
    
    return request_uri

def get_google_user_info(code: str) -> Dict[str, Any]:
    """
    Get user info from Google using authorization code
    """
    try:
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        
        # Prepare and send a request to get tokens
        token_url, headers, body = prepare_token_request(
            token_endpoint,
            authorization_response=f"{settings.OAUTH_REDIRECT_URI}?code={code}",
            redirect_url=settings.OAUTH_REDIRECT_URI,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
        )
        
        # Log request details for debugging (only in development)
        print(f"Token request URL: {token_url}")
        print(f"Token request body: {body}")
        
        # Get tokens
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
        )
        
        # Log token response for debugging
        print(f"Token response status: {token_response.status_code}")
        if token_response.status_code != 200:
            print(f"Token response error: {token_response.text}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not retrieve token from Google: {token_response.text}"
            )
        
        # Parse the tokens
        tokens = token_response.json()
        
        # Get user info using the access token
        userinfo_response = requests.get(
            userinfo_endpoint,
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )
        
        # Log userinfo response for debugging
        print(f"Userinfo response status: {userinfo_response.status_code}")
        if userinfo_response.status_code != 200:
            print(f"Userinfo response error: {userinfo_response.text}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Could not retrieve user info from Google: {userinfo_response.text}"
            )
        
        return userinfo_response.json()
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        # Log the error and raise a readable error
        print(f"Error in get_google_user_info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process Google authentication: {str(e)}"
        )

def prepare_token_request(
    token_endpoint: str,
    authorization_response: str,
    redirect_url: str,
    client_id: str,
    client_secret: str,
) -> tuple:
    """
    Prepare token request for Google OAuth
    """
    # Extract code safely from the authorization_response
    code = authorization_response.split("code=")[1]
    # Remove any additional query parameters if present
    if "&" in code:
        code = code.split("&")[0]
        
    return (
        token_endpoint,
        {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        {
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_url,
            "grant_type": "authorization_code",
        },
    )

def authenticate_user(db: Session, code: str) -> Token:
    """
    Authenticate user with Google OAuth
    """
    # Get user info from Google
    user_info = get_google_user_info(code)
    
    # Create user if not exists
    user_data = UserCreate(
        email=user_info["email"],
        google_id=user_info["sub"],
    )
    
    user = get_or_create_user(db, user_data)
    
    # Create access token
    access_token = create_access_token(subject=user.id)
    
    return Token(access_token=access_token) 
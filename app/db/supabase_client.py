from supabase import create_client, Client
from app.core.config import settings

# Global client instance
_supabase_client = None


def get_supabase_client() -> Client:
    """
    Returns a singleton Supabase client instance.
    Creates it on first call, returns the existing instance on subsequent calls.
    """
    global _supabase_client

    if _supabase_client is None:
        _supabase_client = create_client(
            settings.SUPABASE_PROJECT_URL,
            settings.SUPABASE_ANON_KEY
        )

    return _supabase_client

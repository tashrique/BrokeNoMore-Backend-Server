import logging
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import os

from app.db.base import Base, engine
from app.core.config import settings

# Import all models to ensure they are registered with SQLAlchemy
from app.db.models import User, Transaction, PurchaseEvaluation, FinancialProfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    """
    Initialize the database: create tables if they don't exist.
    """
    # Check if database file exists (for SQLite), if not, ensure directory exists
    if settings.DATABASE_URL.startswith('sqlite'):
        db_file = settings.DATABASE_URL.replace('sqlite:///', '')
        db_dir = os.path.dirname(db_file)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
    # Create database if it doesn't exist (for non-SQLite databases)
    if not settings.DATABASE_URL.startswith('sqlite'):
        if not database_exists(engine.url):
            create_database(engine.url)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

if __name__ == "__main__":
    logger.info("Creating database tables...")
    init_db()
    logger.info("Database initialization completed.") 
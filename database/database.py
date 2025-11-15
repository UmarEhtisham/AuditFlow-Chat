from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create async SQLAlchemy engine
# Read-only behavior will be enforced at the application level
engine = create_async_engine(DATABASE_URL)

# Create an async configured "AsyncSessionLocal" class using async_sessionmaker
# All database operations in this application are read-only by design
async_sessionmaker_obj = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Create a Base class for declarative models
Base = declarative_base()


@asynccontextmanager
async def get_db_session():
    """
    Async context manager for database sessions
    NOTE: This session is used for read-only operations only
    """
    async with async_sessionmaker_obj() as db:
        try:
            yield db
        finally:
            await db.close()
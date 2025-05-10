from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import os

load_dotenv()
# Database connection URL
# DATABASE_URL = ""

DATABASE_URL = os.getenv("DATABASE_URL")
# Check if DATABASE_URL is set correctly
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set.")
<<<<<<< HEAD

print(f"Connecting to database at {DATABASE_URL}")
=======
>>>>>>> f6b54c0aebf55d60193e2b9fac10e519fb07bb77
# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Dependency to get DB session
def get_db():
    with Session(engine) as session:
        yield session

# Function to create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
import dotenv

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///dhvani.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base = declarative_base() #This tells SQLAlchemy that This class represents a table.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.config import Config
import os

config = Config()

if not os.path.exists("database"):
    os.makedirs("database")

db_path = "sqlite:///database/game_of_life.db"

engine = create_engine(
    db_path,
    pool_size=20,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

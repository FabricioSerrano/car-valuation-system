from sqlalchemy import create_engine
from utils.configs import DATABASE_URL
from sqlalchemy.orm import declarative_base

base = declarative_base()


if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in environment variables.")

engine = create_engine(DATABASE_URL, future=True)




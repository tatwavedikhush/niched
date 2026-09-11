from sqlalchemy import create_engine, text
from models import Base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://niched:niched@localhost:5433/niched"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.scalar())

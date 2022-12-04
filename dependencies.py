from sqlmodel import Session
from database import engine


# session dependency injection
def get_session():
    with Session(engine) as session:
        yield session
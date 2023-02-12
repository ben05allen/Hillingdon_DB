from datetime import date
from typing import Optional
from sqlmodel import create_engine

from models import SQLModel


sqlite_filename = "hillingdon.db"
sqlite_url = f"sqlite:///{sqlite_filename}"
engine = create_engine(sqlite_url, echo=False)




def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    

if __name__ == '__main__':
    create_db_and_tables()

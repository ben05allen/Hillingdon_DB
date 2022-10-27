from datetime import date
from typing import Optional, List
from sqlmodel import SQLModel, create_engine, Field, Relationship


sqlite_filename = "hillingdon.db"
sqlite_url = f"sqlite:///{sqlite_filename}"
engine = create_engine(sqlite_url, echo=False)


class Rider(SQLModel, table=True):
    rider_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    isJunior: bool
    isFemale: bool

    results: List['EventResult'] =  Relationship(back_populates='rider')


class Event(SQLModel, table=True):
    event_id: int = Field(default=None, primary_key=True)
    date: date

    results: List['EventResult'] = Relationship(back_populates='event')


class EventResult(SQLModel, table=True):
    results_id: Optional[int] = Field(default=None, primary_key=True)
    event_id: Optional[int] = Field(default=None, foreign_key='event.event_id')
    rider_id: Optional[int] = Field(default=None, foreign_key='rider.rider_id')
    category: str
    total_time: str
    fastest_lap_time: Optional[str] = Field(default=None)
    fastest_lap: Optional[int] = Field(default=None)
    laps_completed: int

    event: Optional[Event] = Relationship(back_populates='results')
    rider: Optional[Rider] = Relationship(back_populates='results')


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    

if __name__ == '__main__':
    create_db_and_tables()

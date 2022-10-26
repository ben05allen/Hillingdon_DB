from datetime import date, timedelta
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Rider(SQLModel, table=True):
    rider_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    isJunior: bool
    isFemale: bool

    results: List['EventResult'] =  Relationship(back_populates='rider')


class Event(SQLModel, table=True):
    event_id: int = Field(primary_key=True)
    date: date

    results: List['EventResult'] = Relationship(back_populates='event')


class EventResult(SQLModel, table=True):
    results_id: Optional[int] = Field(default=None, primary_key=True)
    event_id: Optional[int] = Field(default=None, foreign_key='event.id')
    rider_id: Optional[int] = Field(default=None, foreign_key='rider.id')
    category: str
    total_time: timedelta
    fastest_lap_time: timedelta
    fastest_lap: int
    laps_completed: int

    event: Optional[Event] = Relationship(back_populates='results')
    rider: Optional[Rider] = Relationship(back_populates='results')
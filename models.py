from typing import Optional
from datetime import date, time

from sqlmodel import SQLModel, Field, Relationship


class Rider(SQLModel, table=True):
    rider_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    isJunior: bool
    isFemale: bool

    results: list['EventResult'] =  Relationship(back_populates='rider')


class Event(SQLModel, table=True):
    event_id: int = Field(default=None, primary_key=True)
    date: date

    results: list['EventResult'] = Relationship(back_populates='event')


class EventResult(SQLModel, table=True):
    results_id: Optional[int] = Field(default=None, primary_key=True)
    event_id: Optional[int] = Field(default=None, foreign_key='event.event_id')
    rider_id: Optional[int] = Field(default=None, foreign_key='rider.rider_id')
    category: str
    total_time: time
    fastest_lap_time: Optional[time] = Field(default=None)
    fastest_lap: Optional[int] = Field(default=None)
    laps_completed: int

    event: Optional[Event] = Relationship(back_populates='results')
    rider: Optional[Rider] = Relationship(back_populates='results')


# class FastestLap(SQLModel):
#     category: str
#     name: str
#     fastest_lap_time: Optional[time]
#     fastest_lap: Optional[int]
#     event_id: int
#     isFemale: bool
#     isJunior: bool


# class FastestEvent(SQLModel):
#     category: str
#     name: str
#     total_time: str
#     event_id: int
#     isFemale: bool
#     isJunior: bool


class Ranking(SQLModel):
    rider_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    seconds: float
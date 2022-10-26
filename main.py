import sys
import json
import datetime
import pathlib
from typing import List, Union

from fastapi import FastAPI, Depends, Response
from sqlmodel import Session, select
from database import engine, Rider, Event, EventResult


app = FastAPI()
home_dir = pathlib.Path('.')


# helper for dependency injection
def get_session():
    with Session(engine) as session:
        yield session


@app.on_event('startup')
async def startup_event():
    with Session(engine) as session:
        statement = select(Event)
        result = session.exec(statement).first()
        if result is None:
            events_path = home_dir / 'data' / 'event_dates.json'
            with open(events_path) as events_file:
                events = json.load(events_file)['data']
                for event in events:
                    session.add(Event(**event))
        session.commit()

        statement = select(Rider)
        result = session.exec(statement).first()
        if result is None:
            riders_path = home_dir / 'data' / 'riders.json'
            with open(riders_path) as riders_file:
                riders = json.load(riders_file)['data']
                for rider in riders:
                    session.add(Rider(**rider))
        session.commit()



@app.get('/')
def home():
    return {'Data': 'Testing'}

    
@app.get('/events/', response_model=List[Event])
def select_events(session: Session = Depends(get_session)):
    statement = select(Event)
    result = session.exec(statement).all()
    return result


@app.get('/event/{event_id}', response_model=Union[Event, str])
def event(event_id: int, response: Response, session: Session = Depends(get_session)):
    track = session.get(Event, event_id)
    if track is None:
        response.status_code = 404
        return "Track no found"
    return track


@app.get('/riders/', response_model=List[Rider])
def select_riders(session: Session = Depends(get_session)):
    statement = select(Rider)
    result = session.exec(statement).all()
    return result


@app.get('/rider/{rider_id}', response_model=Union[Rider, str])
def rider(rider_id: int, response: Response, session: Session = Depends(get_session)):
    track = session.get(Rider, rider_id)
    if track is None:
        response.status_code = 404
        return "Track no found"
    return track



# @app.post('/create-rider/{rider_id}')
# def create_rider(rider_id: int, rider: Rider):
#     if rider_id in rider:
#         return {'Error': f'Rider ID {rider_id} already exists'}
    
#     riders[rider_id] = rider
#     return riders[rider_id]




def main():
    pass
        
if __name__ == '__main__':

    if '--help' in sys.argv:
        print('Usage: uvicorn main:app --reload')

    else:
        main()
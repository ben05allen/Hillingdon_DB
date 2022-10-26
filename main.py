import sys
import json
import datetime
import pathlib
from typing import List, Union

from fastapi import FastAPI, Depends, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlmodel import Session, select
from database import engine, Rider, Event, EventResult


app = FastAPI()
home_dir = pathlib.Path('.')
templates = Jinja2Templates(directory="templates")



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




@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('index.html', context)

    
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

@app.post('/event/', response_model=Event, status_code=201)
def create_event(event: Event, session: Session = Depends(get_session)):
    session.add(event)
    session.commit()
    session.refresh(event)


@app.put('/event/{event_id}', response_model=Union[Event, str])
def update_event(event_id: int, updated_event: Event, response: Response, session: Session = Depends(get_session)):
    
    event = session.get(Event, event_id)
    if event is None:
        response.status_code = 404
        return 'Event not found'

    event_dict = updated_event.dict(exclude_unset=True)
    for key ,val in event_dict.items():
        setattr(event, key, val)
    try:
        session.add(event)
    except:
        session.rollback()
        return 'Internal error'
    else:
        session.commit()
        session.refresh(event)
        return event


@app.delete('/event/{event_id}', response_model=str, status_code=201)
def delete_event(event_id: int, response: Response, session: Session = Depends(get_session)):

    event = session.get(Event, event_id)
    if event is None:
        response.status_code = 404
        return 'Event not found'
    try:    
        session.delete(event)
    except:
        session.rollback()
        return Response(status_code=500)
    else:
        session.commit()
        return Response(status_code=200)
    


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


@app.post('/rider/', response_model=Rider, status_code=201)
def create_rider(rider: Rider, session: Session = Depends(get_session)):
    session.add(rider)
    session.commit()
    session.refresh(rider)



def main():
    pass
        
if __name__ == '__main__':

    if '--help' in sys.argv:
        print('Usage: uvicorn main:app --reload')

    else:
        main()
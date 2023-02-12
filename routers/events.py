from fastapi import APIRouter, Depends, Response
from sqlmodel import select, Session

from models import Event
from dependencies import get_session

router = APIRouter()


@router.get('s/', response_model=list[Event])
def select_event_results(session: Session = Depends(get_session)):
    statement = select(Event)
    return session.exec(statement).all()


@router.get('/{event_id}', response_model=Event|str)
def event_result(event_id: int, response: Response, session: Session = Depends(get_session)):
    track = session.get(Event, event_id)
    if track is None:
        response.status_code = 404
        return "Track no found"
    return track


@router.post('/', response_model=Event, status_code=201)
def create_event_result(event_result: Event, session: Session = Depends(get_session)):
    session.add(event_result)
    session.commit()
    session.refresh(event_result)


@router.put('/{event_id}', response_model=Event|str)
def update_event_result(event_id: int, updated_event_result: Event, response: Response, session: Session = Depends(get_session)):
    event_result = session.get(Event, event_id)
    if event_result is None:
        response.status_code = 404
        return 'Event not found'

    event_result_dict = updated_event_result.dict(exclude_unset=True)
    for key ,val in event_result_dict.items():
        setattr(event_result, key, val)
    try:
        session.add(event_result)
    except:
        session.rollback()
        return 'Internal error'
    else:
        session.commit()
        session.refresh(event_result)
        return event_result


@router.delete('/{event_id}', response_model=str, status_code=201)
def delete_event_result(event_id: int, response: Response, session: Session = Depends(get_session)):
    event_result = session.get(Event, event_id)
    if event_result is None:
        response.status_code = 404
        return 'Event not found'
    try:    
        session.delete(event_result)
    except:
        session.rollback()
        return Response(status_code=500)
    else:
        session.commit()
        return Response(status_code=200)
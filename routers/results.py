from sys import prefix
from typing import List, Union
from fastapi import APIRouter, Depends, Response
from sqlmodel import Session, select
from database import engine, EventResult
from ..dependencies import get_session

router = APIRouter(prefix='/event_result', tags=['results'])


@router.get('s/', response_model=List[EventResult])
def select_event_results(session: Session = Depends(get_session)):
    statement = select(EventResult)
    result = session.exec(statement).all()
    return result


@router.get('/{event_result_id}', response_model=Union[EventResult, str])
def event_result(event_result_id: int, response: Response, session: Session = Depends(get_session)):
    track = session.get(EventResult, event_result_id)
    if track is None:
        response.status_code = 404
        return "Track no found"
    return track


@router.post('/', response_model=EventResult, status_code=201)
def create_event_result(event_result: EventResult, session: Session = Depends(get_session)):
    session.add(event_result)
    session.commit()
    session.refresh(event_result)


@router.put('/{event_result_id}', response_model=Union[EventResult, str])
def update_event_result(event_result_id: int, updated_event_result: EventResult, response: Response, session: Session = Depends(get_session)):
    
    event_result = session.get(EventResult, event_result_id)
    if event_result is None:
        response.status_code = 404
        return 'EventResult not found'

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


@router.delete('/{event_result_id}', response_model=str, status_code=201)
def delete_event_result(event_result_id: int, response: Response, session: Session = Depends(get_session)):

    event_result = session.get(EventResult, event_result_id)
    if event_result is None:
        response.status_code = 404
        return 'EventResult not found'
    try:    
        session.delete(event_result)
    except:
        session.rollback()
        return Response(status_code=500)
    else:
        session.commit()
        return Response(status_code=200)
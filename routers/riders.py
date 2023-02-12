from fastapi import APIRouter, Depends, Response
from sqlmodel import select, Session

from models import Rider
from dependencies import get_session

router = APIRouter()


@router.get('s/', response_model=list[Rider])
def select_riders(session: Session = Depends(get_session)):
    statement = select(Rider)
    return session.exec(statement).all()


@router.get('/{rider_id}', response_model=Rider|str)
def rider(rider_id: int, response: Response, session: Session = Depends(get_session)):
    rider = session.get(Rider, rider_id)
    if rider is None:
        response.status_code = 404
        return "Rider no found"
    return rider


@router.post('/', response_model=Rider, status_code=201)
def create_rider(rider: Rider, session: Session = Depends(get_session)):
    session.add(rider)
    session.commit()
    session.refresh(rider)


@router.put('/{rider_id}', response_model=Rider|str)
def update_rider(rider_id: int, updated_rider: Rider, response: Response, session: Session = Depends(get_session)):
    
    rider = session.get(Rider, rider_id)
    if rider is None:
        response.status_code = 404
        return 'Rider not found'

    rider_dict = updated_rider.dict(exclude_unset=True)
    for key ,val in rider_dict.items():
        setattr(rider, key, val)
    try:
        session.add(rider)
    except:
        session.rollback()
        return 'Internal error'
    else:
        session.commit()
        session.refresh(rider)
        return rider


@router.delete('/{rider_id}', response_model=str, status_code=201)
def delete_rider(rider_id: int, response: Response, session: Session = Depends(get_session)):

    rider = session.get(Rider, rider_id)
    if rider is None:
        response.status_code = 404
        return 'Rider not found'
    try:    
        session.delete(rider)
    except:
        session.rollback()
        return Response(status_code=500)
    else:
        session.commit()
        return Response(status_code=200)

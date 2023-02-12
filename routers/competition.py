from enum import Enum
from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlmodel import select, Session, and_, or_

from models import EventResult, Rider, Ranking
from dependencies import get_session


router = APIRouter()


class CategoryName(str, Enum):
    frb = "frb"
    ftt = "ftt"
    jfrb = "jfrb"
    jftt = "jftt"
    jrb = "jrb"
    jtt = "jtt"
    rb = "rb"
    tt = "tt"


def seconds(time: datetime.time) -> float:
    return 3600*time.hour + 60*time.minute + time.second + time.microsecond/1_000_000


@router.get('/{category}', response_model=list[Ranking])
def fastest_riders(category: CategoryName, session: Session = Depends(get_session)):

    # get eligible riders
    if category.value[0] == 'f':
        statement = select(Rider).where(Rider.isFemale==True)
    elif category.value[:2] == 'jf':
        statement = select(Rider).where(and_(Rider.isFemale==True, Rider.isJunior==True))
    elif category.value[0] == 'j':
        statement = select(Rider).where(Rider.isJunior==True)
    else:
        statement = select(Rider)

    riders = session.exec(statement).all()
    eligible_riders = {rider.rider_id: rider.name for rider in riders}

    # get bike category
    if 'rb' in category.value:
        statement = select(EventResult).where(and_(
            EventResult.rider_id.in_(eligible_riders),
            EventResult.category.in_(['RB','JRB','FRB','JFRB'])
        ))
    else:
        statement = select(EventResult).where(EventResult.rider_id.in_(eligible_riders)) 
            
    all_results = session.exec(statement).all()
    grouped_results = defaultdict(list)
    for result in all_results:
        grouped_results[result.rider_id].append(result.total_time)

    print(grouped_results[76])

    # take only results for riders with 6 or more results
    return sorted([Ranking(**{'rider_id': rider_id, 
                'name': eligible_riders[rider_id], 
                'seconds': sum(sorted(map(seconds, times))[:6])} ) 
                for rider_id, times in grouped_results.items() if len(times) >= 6],
                key=lambda x: x.seconds)






# @router.get('/{category}', response_model=list[Ranking])
# def select_event_results(session: Session = Depends(get_session)):
#     statement = select(Event)
#     return session.exec(statement).all()
from enum import Enum
from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlmodel import select, Session, and_

from models import EventResult, Rider, Ranking, FastestEvent, FastestLap
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


def to_seconds(time: datetime.time) -> float:
    return 3600*time.hour + 60*time.minute + time.second + time.microsecond/1_000_000


def riders_by_category(category: CategoryName, session: Session) -> list[Rider]:
    """get eligible riders"""
    if category.value[0] == 'f':
        statement = select(Rider).where(Rider.isFemale==True)
    elif category.value[:2] == 'jf':
        statement = select(Rider).where(and_(Rider.isFemale==True, Rider.isJunior==True))
    elif category.value[0] == 'j':
        statement = select(Rider).where(Rider.isJunior==True)
    else:
        statement = select(Rider)

    return session.exec(statement).all()


def riders_by_race_type(category: CategoryName, riders: dict, session: Session) -> list[EventResult]:
    """get results by race type"""
    if 'rb' in category.value:
        statement = select(EventResult).where(and_(
            EventResult.rider_id.in_(riders),
            EventResult.category.in_(['RB','JRB','FRB','JFRB'])
        ))
    else:
        statement = select(EventResult).where(EventResult.rider_id.in_(riders)) 
            
    return session.exec(statement).all()


@router.get('/{category}', response_model=list[Ranking])
def fastest_riders(category: CategoryName, session: Session = Depends(get_session)):

    eligible_riders = {rider.rider_id: rider.name for rider in riders_by_category(category, session)}
    all_results = riders_by_race_type(category, eligible_riders, session)
    
    grouped_results = defaultdict(list)
    for result in all_results:
        grouped_results[result.rider_id].append(result.total_time)
    
    # take only results for riders with 6 or more results
    return sorted([Ranking(**{'rider_id': rider_id, 
                'name': eligible_riders[rider_id], 
                'seconds': sum(sorted(map(to_seconds, times))[:6])} ) 
                for rider_id, times in grouped_results.items() if len(times) >= 6],
                key=lambda x: x.seconds)


@router.get('/fastest/lap/{category}', response_model=list[FastestLap])
def fastest_laps(category: CategoryName, session: Session = Depends(get_session)):

    eligible_riders = {rider.rider_id: rider.name for rider in riders_by_category(category, session)}
    results = riders_by_race_type(category, eligible_riders, session)

    rider_results = defaultdict(list)
    for result in results:
        if result.fastest_lap_time:
            rider_results[result.rider_id].append(result)

    fastest_results = [min(rider_result, key=lambda x: x.fastest_lap_time) for rider_result in rider_results.values()]

    return sorted([FastestLap(**{'rider_id': result.rider_id, 
        'name': eligible_riders[result.rider_id],
        'fastest_lap_time': result.fastest_lap_time,
        'fastest_lap': result.fastest_lap,
        'event_id': result.event_id}) 
        for result in fastest_results],
        key=lambda x: x.fastest_lap_time)


@router.get('/fastest/event/{category}', response_model=list[FastestEvent])
def fastest_events(category: CategoryName, session: Session = Depends(get_session)):

    eligible_riders = {rider.rider_id: rider.name for rider in riders_by_category(category, session)}
    results = riders_by_race_type(category, eligible_riders, session)

    rider_results = defaultdict(list)
    for result in results:
        if result.laps_completed == 11:
            rider_results[result.rider_id].append(result)

    fastest_results = [min(rider_result, key=lambda x: x.total_time) for rider_result in rider_results.values()]

    return sorted([FastestEvent(**{'rider_id': result.rider_id, 
        'name': eligible_riders[result.rider_id],
        'total_time': result.total_time,
        'event_id': result.event_id}) 
        for result in fastest_results],
        key=lambda x: x.total_time)

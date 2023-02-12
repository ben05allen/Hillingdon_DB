import pathlib

from fastapi import FastAPI, Depends, Response, Request
from fastapi.responses import HTMLResponse


from routers import home
from routers import competition
from routers import results
from routers import riders
from routers import events


app = FastAPI()
home_dir = pathlib.Path('.')

app.include_router(home.router)

app.include_router(competition.router,
    prefix='/competition', 
    tags=['competition'])

app.include_router(results.router,
    prefix='/event_result', 
    tags=['results'])

app.include_router(riders.router,
    prefix='/rider', 
    tags=['riders'])

app.include_router(events.router,
    prefix='/event', 
    tags=['events'])



# @app.on_event('startup')
# async def startup_event():
#     with Session(engine) as session:
#         statement = select(Event)
#         if session.exec(statement).first() is None:
#             events_path = home_dir / 'data' / 'event_dates.json'
#             with open(events_path) as events_file:
#                 events = json.load(events_file)['data']
#                 for event in events:
#                     session.add(Event(**event))
#                 session.commit()

#         statement = select(Event)
#         if session.exec(statement).first() is None:
#             riders_path = home_dir / 'data' / 'riders.json'
#             with open(riders_path) as riders_file:
#                 riders = json.load(riders_file)['data']
#                 for rider in riders:
#                     session.add(Event(**rider))
#                 session.commit()

#         statement = select(EventResult)
#         if session.exec(statement).first() is None:
#             results_path = home_dir / 'data' / 'results.json'
#             with open(results_path) as results_file:
#                 results = json.load(results_file)['data']
#                 for result in results:
#                     session.add(EventResult(**result))
#                 session.commit()


# @app.get('/fastestlaps/', response_model=List[FastestLap])
# def select_fastest_laps(response: Response, session: Session = Depends(get_session)):
#     statement = "SELECT * FROM Fastest_Laps"
#     fastest_laps = session.exec(statement)
#     return fastest_laps.all()


# @app.get('/{category}_ranking/', response_model=List[Ranking])
# def select_ranking(category: CategoryName, session: Session = Depends(get_session)):
#     statement = f"SELECT * FROM {category}_Ranking"
#     ranking = session.exec(statement)
#     return ranking.all()


# @app.get('/fastestevents/', response_model=List[FastestEvent])
# def select_fastest_laps(response: Response, session: Session = Depends(get_session)):
#     statement = "SELECT * FROM Fastest_Events"
#     fastest_laps = session.exec(statement)
#     return fastest_laps.all()

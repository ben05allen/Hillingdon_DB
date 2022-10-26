import sys
import datetime
from fastapi import FastAPI, Path, Query, HTTPException, status

from models import SQLModel
from database import engine

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI()


def main():


    @app.get('/')
    def home():
        return {'Data': 'Testing'}

    events = {
        1: {
            'Title': 'Event 1',
            'Date': datetime.date(2022, 5, 4)
        },
        2: {
            'Title': 'Event 2',
            'Date': datetime.date(2022, 5, 18)
        },
        3: {
            'Title': 'Event 3',
            'Date': datetime.date(2022, 6, 1)
        },
        4: {
            'Title': 'Event 4',
            'Date': datetime.date(2022, 6, 15)
        },
        5: {
            'Title': 'Event 5',
            'Date': datetime.date(2022, 6, 29)
        },
        6: {
            'Title': 'Event 6',
            'Date': datetime.date(2022, 7, 13)
        },
        7: {
            'Title': 'Event 7',
            'Date': datetime.date(2022, 7, 27)
        },
        8: {
            'Title': 'Event 8',
            'Date': datetime.date(2022, 8, 10)
        },
        9: {
            'Title': 'Event 9',
            'Date': datetime.date(2022, 8, 24)
        }
    }

    riders = {}

    @app.get('/get-event/{event_id}')
    def get_event(event_id: int = Path(None, description='The ID of the event', gt=0, le=max(events))):
        if event_id not in events:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Event {event_id} not found.')
        
        return events[event_id]

    @app.post('/create-rider/{rider_id}')
    def create_rider(rider_id: int, rider: Rider):
        if rider_id in rider:
            return {'Error': f'Rider ID {rider_id} already exists'}
        
        riders[rider_id] = rider
        return riders[rider_id]
        
if __name__ == '__main__':
   
    if '--help' in sys.argv:
        print('Usage: uvicorn main:app --reload')

    else:
        main()
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from routers.competition import CategoryName
from routers.competition import fastest_riders


templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get('/', response_class=HTMLResponse)
def home(request: Request):
    context = {'request': request, 'competition_results': [1,2,3,4]}
    return templates.TemplateResponse('index.html', context)

# @router.post('/')
# def get_category(category: str):


"""python -m uvicorn file:app --reload"""
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/sources', StaticFiles(directory='sources'), name='sources')
templates = Jinja2Templates(directory='templates')

white_urls = ['/', '/home', '/login', '/logout', '/register', '/main', '/404']


def current_name(request: Request) -> str:
    """Имя вошедшего пользователя из cookie (или «красотка», если не входил)."""
    return request.cookies.get('username') or 'красотка'


@app.get('/', response_class=HTMLResponse)
def main_page(request: Request):
    return templates.TemplateResponse(
        request=request, name='home.html', context={'username': current_name(request)})


@app.get('/home', response_class=HTMLResponse)
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request, name='home.html', context={'username': current_name(request)})


@app.get('/login', response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')


@app.get('/register', response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name='register.html')


@app.get('/main', response_class=HTMLResponse)
def cabinet_page(request: Request):
    return templates.TemplateResponse(request=request, name='main.html')


@app.get('/logout')
def logout():
    response = RedirectResponse(url='/login')
    response.delete_cookie('username')
    return response


@app.get('/404', response_class=HTMLResponse)
def oshibka_page(request: Request):
    return templates.TemplateResponse(request=request, name='404.html')


@app.exception_handler(StarletteHTTPException)
async def not_found_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(request=request, name='404.html', status_code=404)
    return await http_exception_handler(request, exc)


@app.post('/login')
def login(username: str = Form(...), password: str = Form(...)):
    print(f'Вошёл пользователь: {username}, его пароль {password}', flush=True)

    response = RedirectResponse(url='/main', status_code=303)
    response.set_cookie('username', username.split('@')[0])  
    return response

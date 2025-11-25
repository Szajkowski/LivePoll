from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import socket
from models import Poll
from routers.polls import router as polls_router
from routers.votes import router as votes_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import os


app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Ścieżka do folderu frontend
FRONTEND_DIR = "frontend"


def get_local_ip():
    """
    Zwraca lokalny adres IP maszyny.

    Funkcja tworzy tymczasowe połączenie UDP do serwera DNS Google
    (nie jest ono faktycznie wykonywane) w celu uzyskania adresu IP
    karty sieciowej, z której domyślnie korzysta system.

    :return: Adres IP hosta.
    :rtype: str
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


@app.on_event("startup")
def print_create_url():
    """
    Wyświetla w konsoli adres URL, pod którym dostępna jest aplikacja.

    Funkcja jest wykonywana automatycznie przy starcie serwera FastAPI.
    Wykorzystuje :func:`get_local_ip` do pobrania adresu sieciowego
    i wypisuje pełny link do strony głównej projektu.
    """
    ip = get_local_ip()
    print(f"\nAplikacja dostępna pod: http://{ip}:8000/\n")


@app.get("/create")
def create_page():
    """
    Zwraca stronę tworzenia ankiety.

    :return: Plik HTML `create.html`.
    :rtype: fastapi.responses.FileResponse
    """
    return FileResponse(os.path.join(FRONTEND_DIR, "create.html"))


@app.get("/error")
def error_page():
    """
    Zwraca stronę błędu dla nieistniejących zasobów.

    :return: Plik HTML `error.html`.
    :rtype: fastapi.responses.FileResponse
    """
    return FileResponse(os.path.join(FRONTEND_DIR, "error.html"))


@app.get("/{poll_id}")
def poll_page(poll_id: str, db: Session = Depends(get_db)):
    """
    Zwraca stronę ankiety o podanym identyfikatorze.

    Jeżeli ankieta nie istnieje, wykonywane jest przekierowanie
    do strony błędu.

    :param poll_id: Identyfikator ankiety.
    :type poll_id: str
    :param db: Sesja bazy danych.
    :type db: sqlalchemy.orm.Session
    :return: Plik HTML `poll.html` lub przekierowanie.
    :rtype: fastapi.responses.FileResponse | fastapi.responses.RedirectResponse
    """
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    if not poll:
        return RedirectResponse("/error")

    return FileResponse(os.path.join(FRONTEND_DIR, "poll.html"))


@app.get("/")
def index_page():
    """
    Zwraca stronę główną listy ankiet.

    :return: Plik HTML `index.html`.
    :rtype: fastapi.responses.FileResponse
    """
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


Base.metadata.create_all(bind=engine)

app.include_router(polls_router)
app.include_router(votes_router)

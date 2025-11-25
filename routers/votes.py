from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Vote
from pydantic import BaseModel
from schemas import VotesPayload
from schemas import VoteCreate

from utils.ws_manager import ws_manager
from routers.polls import poll_results

router = APIRouter(prefix="/votes", tags=["votes"])

@router.post("/")
async def create_votes(payload: VotesPayload, db: Session = Depends(get_db)):
    """ Zapisuje głosy użytkownika w bazie danych i aktualizuje wyniki ankiety. Jeśli użytkownik już wcześniej głosował w tej ankiecie (sprawdzane po session_id), nowe głosy nie są zapisywane.
    :param payload: Dane głosów przesłanych przez użytkownika.
    :type payload: VotesPayload
    :param db: Sesja bazy danych.
    :type db: sqlalchemy.orm.Session
    :return: Status zapisu głosów.
    :rtype: dict
    """
    poll_id = payload.votes[0].poll_id
    session_id = payload.votes[0].session_id
    # sprawdź, czy user już głosował
    exists = (db.query(Vote).filter(Vote.poll_id == poll_id, Vote.session_id == session_id).first())
    if exists:
        return {"status": "ignored", "reason": "already_voted"}

    for v in payload.votes:
        vote = Vote( poll_id=v.poll_id,
                     question_id=v.question_id,
                     answer_id=v.answer_id,
                     session_id=v.session_id
                     )
        db.add(vote)

    db.commit()

    # broadcast
    new_results = poll_results(poll_id, db)
    await ws_manager.broadcast(poll_id, {"results": new_results})

    return {"status": "ok"}

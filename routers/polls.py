from fastapi import APIRouter, Depends, WebSocket, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models import Poll, Question, Answer, QuestionType, Vote
from schemas import PollCreate, PollResponse, DeleteRequest, PollUpdate

from utils.ws_manager import ws_manager   # ✅ NEW

router = APIRouter(prefix="/polls", tags=["polls"])


@router.get("/list")
def list_polls(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    """
        Zwraca listę ankiet z paginacją.

        :param page: Numer strony.
        :type page: int
        :param limit: Liczba ankiet na stronę.
        :type limit: int
        :param db: Sesja bazy danych.
        :type db: sqlalchemy.orm.Session
        :return: Struktura zawierająca listę ankiet, aktualną stronę, limit i łączną liczbę ankiet.
        :rtype: dict
    """
    if page < 1:
        page = 1

    total = db.query(Poll).count()
    polls = (
        db.query(Poll)
        .order_by(Poll.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "polls": [
            {
                "id": p.id,
                "title": p.title,
            }
            for p in polls
        ]
    }


def validate_poll(data: PollCreate):
    """
    Waliduje dane ankiety przed zapisaniem.

    Sprawdza obecność tytułu, pytań, odpowiedzi oraz duplikaty odpowiedzi.

    :param data: Dane ankiety do walidacji.
    :type data: PollCreate
    :return: Lista komunikatów błędów. Pusta lista oznacza brak błędów.
    :rtype: list[str]
    """
    errors = []

    if not data.title or not data.title.strip():
        errors.append("Tytuł ankiety jest wymagany.")

    if not data.questions or len(data.questions) == 0:
        errors.append("Ankieta musi zawierać co najmniej jedno pytanie.")
        return errors   # reszta walidacji zbędna

    for i, q in enumerate(data.questions, start=1):
        if not q.text or not q.text.strip():
            errors.append(f"Pytanie #{i} musi mieć treść.")

        if not q.answers or len(q.answers) == 0:
            errors.append(f"Pytanie #{i} musi mieć co najmniej jedną odpowiedź.")
            continue

        # --- SPRAWDZENIE DUPLIKATÓW ODPOWIEDZI ---
        normalized = [a.text.strip() for a in q.answers if a.text]
        duplicates = set([ans for ans in normalized if normalized.count(ans) > 1])
        if duplicates:
            dup_str = ", ".join(sorted(duplicates))
            errors.append(f"Pytanie #{i} zawiera zduplikowane odpowiedzi: {dup_str}")

        for j, a in enumerate(q.answers, start=1):
            if not a.text or not a.text.strip():
                errors.append(f"Odpowiedź #{j} w pytaniu #{i} musi mieć treść.")

    return errors


@router.post("/")
def create_poll(data: PollCreate, db: Session = Depends(get_db)):
    """
    Tworzy nową ankietę w bazie danych.

    :param data: Dane nowej ankiety.
    :type data: PollCreate
    :param db: Sesja bazy danych.
    :type db: sqlalchemy.orm.Session
    :return: Wynik operacji z informacją o sukcesie lub błędach walidacji.
    :rtype: dict
    """
    errors = validate_poll(data)
    if errors:
        return {
            "ok": False,
            "errors": errors
        }

    poll = Poll(title=data.title)

    for q in data.questions:
        question = Question(
            text=q.text,
            type=QuestionType(q.type)
        )

        for ans in q.answers:
            answer = Answer(text=ans.text)
            question.answers.append(answer)

        poll.questions.append(question)

    db.add(poll)
    db.commit()
    db.refresh(poll)

    return {
        "ok": True,
        "poll_id": poll.id
    }


@router.get("/{poll_id}")
def get_poll(
    poll_id: str,
    session_id: str | None = Query(None),
    db: Session = Depends(get_db)
):
    """
    Pobiera ankietę o podanym identyfikatorze wraz z głosami użytkownika.

    :param poll_id: Identyfikator ankiety.
    :type poll_id: str
    :param session_id: Opcjonalny identyfikator sesji użytkownika, aby pobrać jego głosy.
    :type session_id: str | None
    :param db: Sesja bazy danych.
    :type db: sqlalchemy.orm.Session
    :return: Dane ankiety wraz z listą pytań i zaznaczonych odpowiedzi użytkownika.
    :rtype: dict
    :raises HTTPException: 404 jeśli ankieta nie istnieje.
    """
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    user_votes = {}
    if session_id:
        votes = (
            db.query(Vote)
            .filter(Vote.poll_id == poll_id, Vote.session_id == session_id)
            .all()
        )
        for v in votes:
            user_votes.setdefault(v.question_id, []).append(v.answer_id)

    return {
        "id": poll.id,
        "title": poll.title,
        "questions": [
            {
                "id": q.id,
                "text": q.text,
                "type": q.type.value,
                "answers": [{"id": a.id, "text": a.text} for a in q.answers],
                "user_selected": user_votes.get(q.id, [])
            }
            for q in poll.questions
        ]
    }


@router.get("/{poll_id}/results")
def poll_results(poll_id: str, db: Session = Depends(get_db)):
    """
    Zwraca wyniki ankiety z liczbą głosów dla każdej odpowiedzi.

    :param poll_id: Identyfikator ankiety.
    :type poll_id: str
    :param db: Sesja bazy danych.
    :type db: sqlalchemy.orm.Session
    :return: Lista pytań z odpowiedziami i liczba oddanych głosów.
    :rtype: list[dict]
    :raises HTTPException: 404 jeśli ankieta nie istnieje.
    """
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    results = []
    for q in poll.questions:
        res = {"id": q.id, "text": q.text, "type": q.type.value, "answers": []}
        for a in q.answers:
            count = db.query(Vote).filter_by(answer_id=a.id).count()
            res["answers"].append({"id": a.id, "text": a.text, "votes": count})
        results.append(res)

    return results


@router.patch("/{poll_id}", response_model=PollResponse)
def update_poll(poll_id: str, data: PollUpdate, db: Session = Depends(get_db)):
    """
    Aktualizuje istniejącą ankietę wraz z pytaniami i odpowiedziami.

    :param poll_id: Identyfikator ankiety do aktualizacji.
    :type poll_id: str
    :param data: Dane do aktualizacji ankiety.
    :type data: PollUpdate
    :param db: Sesja bazy danych.
    :type db: sqlalchemy.orm.Session
    :return: Zaktualizowana ankieta.
    :rtype: PollResponse
    :raises HTTPException: 404 jeśli ankieta nie istnieje.
    """
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")

    # update title
    poll.title = data.title

    # map existing items
    existing_q = {q.id: q for q in poll.questions}
    incoming_q_ids = set()

    for q_data in data.questions:
        if q_data.id and q_data.id in existing_q:
            q = existing_q[q_data.id]
            q.text = q_data.text
            q.type = q_data.type
        else:
            q = Question(text=q_data.text, type=q_data.type, poll_id=poll.id)
            db.add(q)
            poll.questions.append(q)

        incoming_q_ids.add(q.id)

        existing_a = {a.id: a for a in q.answers}
        incoming_a_ids = set()

        for a_data in q_data.answers:
            if a_data.id and a_data.id in existing_a:
                a = existing_a[a_data.id]
                a.text = a_data.text
            else:
                a = Answer(text=a_data.text, question_id=q.id)
                db.add(a)
                q.answers.append(a)

            incoming_a_ids.add(a.id)

        # delete removed answers
        for a_id, a in list(existing_a.items()):
            if a_id not in incoming_a_ids:
                db.query(Vote).filter_by(answer_id=a_id).delete()
                db.delete(a)

    # delete removed questions
    for q_id, q in list(existing_q.items()):
        if q_id not in incoming_q_ids:
            # remove answers + votes
            for a in q.answers:
                db.query(Vote).filter_by(answer_id=a.id).delete()
                db.delete(a)
            db.delete(q)

    db.commit()
    db.refresh(poll)

    return poll


@router.delete("/delete")
def delete_record(data: DeleteRequest, db: Session = Depends(get_db)):
    """
    Usuwa obiekt w systemie: ankietę, pytanie, odpowiedź lub głos.

    :param data: Dane określające typ i identyfikator obiektu do usunięcia.
    :type data: DeleteRequest
    :param db: Sesja bazy danych.
    :type db: sqlalchemy.orm.Session
    :return: Informacja o usuniętym obiekcie.
    :rtype: dict
    :raises HTTPException: 404 jeśli obiekt nie istnieje, 400 dla nieznanego typu.
    """
    t = data.type
    i = data.id

    if t == "poll":
        poll = db.query(Poll).filter(Poll.id == i).first()
        if not poll:
            raise HTTPException(404, "Poll not found")

        for q in poll.questions:
            for a in q.answers:
                db.query(Vote).filter_by(answer_id=a.id).delete()
                db.delete(a)
            db.delete(q)
        db.delete(poll)
        db.commit()
        return {"deleted": "poll"}

    elif t == "question":
        q = db.query(Question).filter(Question.id == i).first()
        if not q:
            raise HTTPException(404, "Question not found")
        for a in q.answers:
            db.query(Vote).filter_by(answer_id=a.id).delete()
            db.delete(a)
        db.delete(q)
        db.commit()
        return {"deleted": "question"}

    elif t == "answer":
        a = db.query(Answer).filter(Answer.id == i).first()
        if not a:
            raise HTTPException(404, "Answer not found")
        db.query(Vote).filter(Vote.answer_id == i).delete()
        db.delete(a)
        db.commit()
        return {"deleted": "answer"}

    elif t == "vote":
        v = db.query(Vote).filter(Vote.id == i).first()
        if not v:
            raise HTTPException(404, "Vote not found")
        db.delete(v)
        db.commit()
        return {"deleted": "vote"}

    else:
        raise HTTPException(400, "Unknown type")

@router.websocket("/{poll_id}/ws")
async def poll_ws(websocket: WebSocket, poll_id: str):
    """
    Obsługuje połączenie WebSocket dla ankiety.

    :param websocket: Obiekt połączenia WebSocket.
    :type websocket: fastapi.WebSocket
    :param poll_id: Identyfikator ankiety, dla której obsługiwany jest WS.
    :type poll_id: str
    """
    await ws_manager.connect(poll_id, websocket)

    try:
        while True:
            await websocket.receive_text()   # nic nie robimy — nasłuch
    except:
        ws_manager.disconnect(poll_id, websocket)


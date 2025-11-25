from pydantic import BaseModel, ConfigDict
from enum import Enum
from models import QuestionType


# ---------- UPDATE ----------
class AnswerUpdate(BaseModel):
    """
    Schemat aktualizacji pojedynczej odpowiedzi.

    :param id: Opcjonalny identyfikator odpowiedzi. Jeżeli istnieje, aktualizuje istniejącą odpowiedź.
    :type id: int | None
    :param text: Treść odpowiedzi.
    :type text: str
    """
    id: int | None
    text: str

class QuestionUpdate(BaseModel):
    """
    Schemat aktualizacji pytania w ankiecie.

    :param id: Opcjonalny identyfikator pytania. Jeżeli istnieje, aktualizuje istniejące pytanie.
    :type id: int | None
    :param text: Treść pytania.
    :type text: str
    :param type: Typ pytania (pojedynczy lub wielokrotny wybór).
    :type type: QuestionType
    :param answers: Lista odpowiedzi powiązanych z pytaniem.
    :type answers: List[AnswerUpdate]
    """
    id: int | None
    text: str
    type: QuestionType
    answers: list[AnswerUpdate]

class PollUpdate(BaseModel):
    """
    Schemat aktualizacji ankiety.

    :param title: Tytuł ankiety.
    :type title: str
    :param questions: Lista pytań w ankiecie.
    :type questions: List[QuestionUpdate]
    """
    title: str
    questions: list[QuestionUpdate]


# ---------- CREATE ----------
class AnswerCreate(BaseModel):
    """
    Schemat tworzenia nowej odpowiedzi.

    :param text: Treść odpowiedzi.
    :type text: str
    """
    text: str

class QuestionCreate(BaseModel):
    """
    Schemat tworzenia nowego pytania.

    :param text: Treść pytania.
    :type text: str
    :param type: Typ pytania (pojedynczy lub wielokrotny wybór).
    :type type: QuestionType
    :param answers: Lista odpowiedzi powiązanych z pytaniem.
    :type answers: List[AnswerCreate]
    """
    text: str
    type: QuestionType
    answers: list[AnswerCreate]

class PollCreate(BaseModel):
    """
    Schemat tworzenia nowej ankiety.

    :param title: Tytuł ankiety.
    :type title: str
    :param questions: Lista pytań w ankiecie.
    :type questions: List[QuestionCreate]
    """
    title: str
    questions: list[QuestionCreate]


# ---------- RESPONSE ----------
class AnswerResponse(BaseModel):
    """
    Schemat odpowiedzi reprezentujący pojedynczą odpowiedź.

    :param id: Identyfikator odpowiedzi.
    :type id: int
    :param text: Treść odpowiedzi.
    :type text: str
    """
    id: int
    text: str

class QuestionResponse(BaseModel):
    """
    Schemat odpowiedzi reprezentujący pytanie w ankiecie.

    :param id: Identyfikator pytania.
    :type id: int
    :param text: Treść pytania.
    :type text: str
    :param type: Typ pytania.
    :type type: QuestionType
    :param answers: Lista odpowiedzi powiązanych z pytaniem.
    :type answers: List[AnswerResponse]
    """
    id: int
    text: str
    type: QuestionType
    answers: list[AnswerResponse]

class PollResponse(BaseModel):
    """
    Schemat odpowiedzi reprezentujący ankietę.

    :param id: Identyfikator ankiety.
    :type id: str
    :param title: Tytuł ankiety.
    :type title: str
    :param questions: Lista pytań w ankiecie.
    :type questions: List[QuestionResponse]
    """
    id: str
    title: str
    questions: list[QuestionResponse]

    model_config = ConfigDict(from_attributes=True)


# ---------- DELETE ----------
class DeleteTarget(str, Enum):
    """
    Typ obiektu do usunięcia.

    :param poll: Ankieta
    :param question: Pytanie
    :param answer: Odpowiedź
    :param vote: Głos
    """
    poll = "poll"
    question = "question"
    answer = "answer"
    vote = "vote"

class DeleteRequest(BaseModel):
    """
    Schemat żądania usunięcia obiektu.

    :param type: Typ obiektu do usunięcia.
    :type type: DeleteTarget
    :param id: Identyfikator obiektu do usunięcia.
    :type id: int | str
    """
    type: DeleteTarget
    id: int | str


# ---------- VOTES ----------
class VoteCreate(BaseModel):
    """
    Model pojedynczego głosu w ankiecie.

    :param poll_id: Identyfikator ankiety.
    :type poll_id: str
    :param question_id: Identyfikator pytania.
    :type question_id: int
    :param answer_id: Identyfikator wybranej odpowiedzi.
    :type answer_id: int
    :param session_id: Unikalny identyfikator sesji użytkownika.
    :type session_id: str
    """
    poll_id: str
    question_id: int
    answer_id: int
    session_id: str


class VotesPayload(BaseModel):
    """
    Model przesyłający listę głosów od użytkownika.

    :param votes: Lista głosów do zapisania.
    :type votes: list[VoteCreate]
    """
    votes: list[VoteCreate]

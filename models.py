from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum
import uuid

def gen_id() -> str:
    """
    Generuje 8-znakowy unikalny identyfikator ankiety.

    :return: Unikalny identyfikator ankiety.
    :rtype: str
    """
    return uuid.uuid4().hex[:8]

class QuestionType(str, enum.Enum):
    """
    Typ pytania w ankiecie.

    :param single: Pojedynczy wybór.
    :type single: str
    :param multi: Wielokrotny wybór.
    :type multi: str
    """
    single = "single"
    multi = "multi"

class Poll(Base):
    """
    Model SQLAlchemy reprezentujący ankietę.

    :param id: Unikalny identyfikator ankiety.
    :type id: str
    :param title: Tytuł ankiety.
    :type title: str
    :param questions: Lista pytań należących do ankiety.
    :type questions: list[Question]
    """
    __tablename__ = "polls"

    id = Column(String(8), primary_key=True, default=gen_id)
    title = Column(String(255), nullable=False)

    questions = relationship("Question", back_populates="poll", cascade="all, delete")

class Question(Base):
    """
    Model SQLAlchemy reprezentujący pytanie w ankiecie.

    :param id: Unikalny identyfikator pytania.
    :type id: int
    :param poll_id: Identyfikator ankiety, do której należy pytanie.
    :type poll_id: str
    :param text: Treść pytania.
    :type text: str
    :param type: Typ pytania (single/multi).
    :type type: QuestionType
    :param poll: Powiązana ankieta.
    :type poll: Poll
    :param answers: Lista odpowiedzi przypisanych do pytania.
    :type answers: list[Answer]
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(String(8), ForeignKey("polls.id"), nullable=False)
    text = Column(String(500), nullable=False)
    type = Column(Enum(QuestionType, native_enum=False), nullable=False)

    poll = relationship("Poll", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete")

class Answer(Base):
    """
    Model SQLAlchemy reprezentujący odpowiedź do pytania.

    :param id: Unikalny identyfikator odpowiedzi.
    :type id: int
    :param question_id: Identyfikator pytania, do którego należy odpowiedź.
    :type question_id: int
    :param text: Treść odpowiedzi.
    :type text: str
    :param question: Powiązane pytanie.
    :type question: Question
    """
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    text = Column(String(500), nullable=False)

    question = relationship("Question", back_populates="answers")

class Vote(Base):
    """
    Model SQLAlchemy reprezentujący głos użytkownika.

    :param id: Unikalny identyfikator głosu.
    :type id: int
    :param poll_id: Identyfikator ankiety.
    :type poll_id: str
    :param question_id: Identyfikator pytania.
    :type question_id: int
    :param answer_id: Identyfikator wybranej odpowiedzi.
    :type answer_id: int
    :param session_id: Identyfikator sesji użytkownika.
    :type session_id: str
    """
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(String(8), ForeignKey("polls.id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))
    answer_id = Column(Integer, ForeignKey("answers.id", ondelete="CASCADE"))
    session_id = Column(String(64), nullable=False)

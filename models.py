from typing import List
from pydantic import BaseModel


class DirectToIndirectSpeechTask(BaseModel):
    id: int
    task: str
    correct_answer: str


class DirectToInderectSpeechCheck(BaseModel):
    id: int
    task: str
    correct_answer: str
    user_answer: str
    is_correct: bool

class VerbTenseTask(BaseModel):
    id: int
    sentence: str
    blanks: List[str]  # This will store the correct answers for each blank
    hints: List[str]   # Optional hints for each blank

class VerbTenseCheck(BaseModel):
    user_answers: List[str]  # User inputs to be checked
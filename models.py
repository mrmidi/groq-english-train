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
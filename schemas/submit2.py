from pydantic import BaseModel

class SubmitRequest(BaseModel):
    question: str

class SubmitResponse(BaseModel):
    # llm_answer: str
    # embedding_result: dict
    db_result: str
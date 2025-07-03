from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/ask")
async def ask_llm(request: Request, question: str):
    client = request.app.state.azure_openai_client
    response = client.chat_completion(question)
    return {"llm_answer": response}

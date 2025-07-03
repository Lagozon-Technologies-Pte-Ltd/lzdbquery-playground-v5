from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/search")
async def search_embeddings(request: Request, query: str):
    collection = request.app.state.schema_collection
    results = collection.query(query_texts=[query], n_results=1)
    return {"embedding_result": results}


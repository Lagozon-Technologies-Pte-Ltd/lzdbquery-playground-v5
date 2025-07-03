from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from schemas.submit2 import SubmitRequest, SubmitResponse
from dependencies import  get_db

router = APIRouter()

@router.post("/submit1", response_model=SubmitResponse)
async def submit1(
    payload: SubmitRequest,
    db: Session = Depends(get_db)
):
    db_result = db.execute("SELECT [part_code] FROM MH_RO_PARTS;")
    rows = db_result.fetchall()  # list of row tuples
    columns = db_result.keys()
    print("db result: ",rows, columns)
    table_name = db_result.fetchone()[0] if db_result.rowcount > 0 else "No tables found"
    return SubmitResponse(
        db_result=table_name
    )
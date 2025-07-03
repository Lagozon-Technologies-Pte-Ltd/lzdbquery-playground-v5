from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

router = APIRouter()

def get_db(request: Request):
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.get("/sample_table")
# def get_sample_table(request: Request, db: Session = Depends(get_db)):
#     result = db.execute("SELECT TOP 1 name FROM sys.tables")
#     table_name = result.fetchone()[0] if result.rowcount > 0 else "No tables found"
#     return {"sample_table": table_name}

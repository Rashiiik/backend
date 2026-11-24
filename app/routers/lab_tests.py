from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import LabTest
from app.schemas import LabTestCreate, LabTestOut

router = APIRouter(prefix="/tests", tags=["Test catalog"])


from fastapi import FastAPI
from app.database import Base, engine
from app import models  
from app.routers import lab_tests       

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ReportBox API")
app.include_router(lab_tests.router)    

@app.get("/health")
def health():
    return {"status": "ok"}

@router.post(
    "",
    response_model=LabTestOut,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Test code already exists"}},
)
def create_test(payload: LabTestCreate, db: Session = Depends(get_db)):
    test = LabTest(**payload.model_dump())
    db.add(test)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Test code '{payload.code}' already exists",
        )
    db.refresh(test)
    return test
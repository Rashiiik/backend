from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models import LabTest
from app.schemas import LabTestCreate, LabTestUpdate, LabTestOut

router = APIRouter(prefix="/tests", tags=["Test catalog"])

NOT_FOUND = {404: {"description": "Test not found"}}


def get_test_or_404(test_id: int, db: Session) -> LabTest:
    test = db.get(LabTest, test_id)
    if test is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")
    return test


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


@router.get("", response_model=list[LabTestOut])
def list_tests(db: Session = Depends(get_db)):
    return db.scalars(select(LabTest).order_by(LabTest.id)).all()


@router.get("/{test_id}", response_model=LabTestOut, responses=NOT_FOUND)
def get_test(test_id: int, db: Session = Depends(get_db)):
    return get_test_or_404(test_id, db)


@router.patch("/{test_id}", response_model=LabTestOut, responses=NOT_FOUND)
def update_test(test_id: int, payload: LabTestUpdate, db: Session = Depends(get_db)):
    test = get_test_or_404(test_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(test, field, value)
    db.commit()
    db.refresh(test)
    return test


@router.delete("/{test_id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND)
def delete_test(test_id: int, db: Session = Depends(get_db)):
    test = get_test_or_404(test_id, db)
    db.delete(test)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
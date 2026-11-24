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


from fastapi import FastAPI

app=FastAPI(title="ReportBox")

@app.get("/health")
def health():
    return {"status" : "ok"}
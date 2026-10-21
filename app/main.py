from fastapi import FastAPI

app = FastAPI(title="FullChair")

# first endpoint
@app.get("/health")
def health():
    return {"ok": True}
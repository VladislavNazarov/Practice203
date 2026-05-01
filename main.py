from fastapi import FastAPI

app = FastAPI(title="Git4CodeSys API")


@app.get("/health")
def health():
    return {"status": "ok"}

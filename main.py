 GNU nano 9.0                        main.py
from fastapi import FastAPI

app = FastAPI(title="Git4CodeSys API")

@app.get("/health")
def health():

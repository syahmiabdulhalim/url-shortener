from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import random
import string


class URLRequest(BaseModel):
    url: str

db = {}
clicks = {}
app = FastAPI()

@app.post("/shorthen-url/")
def shorthen_url(request: URLRequest):
    code = "".join(random.choices(string.ascii_letters, k=6))
    db[code] = request.url
    return {"short_url": f"http://localhost:8000/{code}"}


@app.get("/{code}")
def redirect_to_url(code:str):
    url = db.get(code)
    if url:
        clicks[code] = clicks.get(code, 0) + 1
        return RedirectResponse(url)
    return {"error": "URL not found"}

@app.get("/{code}/stats")
def get_stats(code:str):
    if code in db:
        return {"clicks": clicks.get(code, 0)}
    return {"error": "URL not found"}
    
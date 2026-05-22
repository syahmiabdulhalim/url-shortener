from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
import sqlite3 
import random
import string


class URLRequest(BaseModel):
    url: str

conn = sqlite3.connect("urls.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS url (short_links TEXT PRIMARY KEY, long_links TEXT NOT NULL, clicks INTEGER DEFAULT 0)")
conn.commit()

app = FastAPI()

@app.post("/shorthen-url/")
def shorthen_url(request: URLRequest):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    code = "".join(random.choices(string.ascii_letters, k=6))
    cursor.execute("INSERT OR REPLACE INTO url (short_links, long_links) VALUES (?, ?)", (code, request.url))
    conn.commit()
    return {"short_url": f"http://localhost:8000/{code}"}


@app.get("/{code}")
def redirect_to_url(code:str):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT long_links FROM url WHERE short_links = ?", (code,))
    result = cursor.fetchone()
    if result:
        url = result[0]
        cursor.execute("UPDATE url SET clicks = clicks + 1 WHERE short_links = ?", (code,))
        conn.commit()
        return RedirectResponse(url)
    return {"error": "URL not found"}

@app.get("/{code}/stats")
def get_stats(code:str):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT clicks FROM url WHERE short_links = ?", (code,))
    result = cursor.fetchone()
    if result:
        return {"clicks": result[0]}
    return {"error": "URL not found"}
    
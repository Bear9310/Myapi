import sqlite3
import secrets
import datetime
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from database import (
    init_db,
    create_api_key,
    validate_api_key,
    increment_request_count,
    list_all_keys,
    delete_api_key,
    reset_daily_counts,
    save_chat_history,
    get_chat_history
)
from brain import get_response

app = FastAPI(
    title="MyAPI - Personal AI",
    description="Your own AI API system built from scratch",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "naim2024"

def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_user = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_pass = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_user and correct_pass):
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return credentials.username

@app.on_event("startup")
def startup():
    init_db()
    print("Database ready!")

class ChatRequest(BaseModel):
    message: str
    history: list = []
    mood: str = "professional"

class CreateKeyRequest(BaseModel):
    key_name: str
    daily_limit: int = 100

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", "r") as f:
        return f.read()

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "time": datetime.datetime.now().isoformat()
    }

@app.post("/v1/chat")
def chat(request: ChatRequest, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No API key provided.")
    if authorization.startswith("Bearer "):
        api_key = authorization[7:]
    else:
        api_key = authorization
    is_valid, info = validate_api_key(api_key)
    if not is_valid:
        raise HTTPException(status_code=403, detail=info)
    history = get_chat_history(api_key)
    reply = get_response(request.message, history, request.mood)
    save_chat_history(api_key, request.message, reply)
    try:
        increment_request_count(api_key, "/v1/chat", "success")
    except TypeError:
        increment_request_count(api_key)
    return {
        "success": True,
        "response": reply,
        "memory_used": len(history)
    }

@app.get("/admin", response_class=HTMLResponse)
def admin_panel():
    with open("admin.html", "r") as f:
        return f.read()

@app.post("/admin/create-key")
def create_key_route(request: CreateKeyRequest, admin: str = Depends(verify_admin)):
    api_key = create_api_key(request.key_name, request.daily_limit)
    return {"success": True, "api_key": api_key}

@app.get("/admin/list-keys")
def list_keys_route(admin: str = Depends(verify_admin)):
    return {"success": True, "keys": list_all_keys()}

@app.delete("/admin/delete-key/{api_key}")
def delete_key_route(api_key: str, admin: str = Depends(verify_admin)):
    delete_api_key(api_key)
    return {"success": True, "message": f"Deleted key: {api_key}"}

@app.delete("/admin/delete-key-by-id/{key_id}")
def delete_key_by_id(key_id: int, admin: str = Depends(verify_admin)):
    conn = sqlite3.connect("myapi.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM api_keys WHERE id = ?", (key_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": f"Deleted key id: {key_id}"}

@app.post("/admin/reset-counts")
def reset_counts_route(admin: str = Depends(verify_admin)):
    reset_daily_counts()
    return {"success": True, "message": "Daily counts reset"}

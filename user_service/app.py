from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="User Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS = [
    {"id": 1, "username": "rajesh", "password": "1234", "name": "Rajesh Kumar"},
    {"id": 2, "username": "priya", "password": "5678", "name": "Priya Sharma"},
    {"id": 3, "username": "admin", "password": "admin123", "name": "Admin User"},
]

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def root():
    return {"service": "user-service", "status": "running", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "UP", "service": "user-service"}

@app.post("/login")
def login(request: LoginRequest):
    for user in USERS:
        if user["username"] == request.username and user["password"] == request.password:
            return {
                "success": True,
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "name": user["name"]
                }
            }
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/users")
def get_users():
    return {
        "count": len(USERS),
        "users": [
            {"id": u["id"], "username": u["username"], "name": u["name"]}
            for u in USERS
        ]
    }

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in USERS:
        if user["id"] == user_id:
            return {"id": user["id"], "username": user["username"], "name": user["name"]}
    raise HTTPException(status_code=404, detail="User not found")

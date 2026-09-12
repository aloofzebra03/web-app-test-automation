from typing import List

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="QA Automation Demo", version="1.0.0")

VALID_EMAIL = "qa@example.com"
VALID_PASSWORD = "Password123"

ITEMS = [
    {"id": 1, "name": "Keyboard"},
    {"id": 2, "name": "Mouse"},
    {"id": 3, "name": "Monitor"},
    {"id": 4, "name": "USB Cable"},
]


class LoginRequest(BaseModel):
    email: str
    password: str


class ProfileRequest(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=18, le=65)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>QA Automation Demo</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 20px; }
        section { border: 1px solid #ddd; border-radius: 8px; padding: 18px; margin: 16px 0; }
        label { display: block; margin: 8px 0 4px; }
        input { width: 100%; max-width: 360px; padding: 8px; }
        button { margin-top: 12px; padding: 8px 14px; cursor: pointer; }
        .status { min-height: 22px; margin-top: 10px; font-weight: bold; }
        ul { padding-left: 22px; }
    </style>
</head>
<body>
    <h1>QA Automation Demo</h1>
    <p id="app-status">Application ready</p>

    <section>
        <h2>Login</h2>
        <label for="email">Email</label>
        <input id="email" type="email" value="qa@example.com" />
        <label for="password">Password</label>
        <input id="password" type="password" value="Password123" />
        <button id="login-btn">Login</button>
        <div id="login-status" class="status"></div>
    </section>

    <section>
        <h2>Create profile</h2>
        <label for="username">Username</label>
        <input id="username" value="tester" />
        <label for="age">Age</label>
        <input id="age" type="number" value="18" />
        <button id="profile-btn">Create profile</button>
        <div id="profile-status" class="status"></div>
    </section>

    <section>
        <h2>Search items</h2>
        <label for="search">Search</label>
        <input id="search" placeholder="e.g. mouse" />
        <button id="search-btn">Search</button>
        <ul id="results"></ul>
    </section>

<script>
async function parseJson(response) {
    try { return await response.json(); } catch (_) { return {}; }
}

document.getElementById("login-btn").addEventListener("click", async () => {
    const response = await fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        })
    });
    const body = await parseJson(response);
    document.getElementById("login-status").textContent =
        response.ok ? body.message : (body.detail || "Login failed");
});

document.getElementById("profile-btn").addEventListener("click", async () => {
    const response = await fetch("/api/profile", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: document.getElementById("username").value,
            age: Number(document.getElementById("age").value)
        })
    });
    const body = await parseJson(response);
    document.getElementById("profile-status").textContent =
        response.ok ? `Profile created for ${body.username}` : "Validation failed";
});

document.getElementById("search-btn").addEventListener("click", async () => {
    const q = encodeURIComponent(document.getElementById("search").value);
    const response = await fetch(`/api/items?q=${q}`);
    const body = await parseJson(response);
    const results = document.getElementById("results");
    results.innerHTML = "";
    body.items.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item.name;
        results.appendChild(li);
    });
});
</script>
</body>
</html>
"""


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/login")
def login(payload: LoginRequest) -> dict:
    if payload.email != VALID_EMAIL or payload.password != VALID_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user": payload.email}


@app.post("/api/profile")
def create_profile(payload: ProfileRequest) -> dict:
    return {
        "message": "Profile created",
        "username": payload.username,
        "age": payload.age,
    }


@app.get("/api/items")
def search_items(q: str = Query(default="")) -> dict:
    normalized = q.strip().lower()
    if not normalized:
        return {"items": ITEMS}
    return {
        "items": [item for item in ITEMS if normalized in item["name"].lower()]
    }

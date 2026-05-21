from fastapi import FastAPI
from fastapi.security import HTTPBearer
from routers import auth, items, users

app = FastAPI()

security = HTTPBearer()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
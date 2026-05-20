from fastapi import FastAPI
from routers import auth, items, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, items, users

app = FastAPI()

security = HTTPBearer()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # default Vite port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
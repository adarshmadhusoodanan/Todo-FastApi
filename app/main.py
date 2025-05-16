import uvicorn
from fastapi import FastAPI

from app.api import routes

from .db.database import create_db_and_tables


# Create FastAPI app
app = FastAPI(title="Todo", description="todo app built with fastapi")


app.include_router(routes.router)   

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()


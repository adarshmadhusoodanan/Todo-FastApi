import uvicorn
from fastapi import FastAPI

from .database import create_db_and_tables

from .routes import auth


# Create FastAPI app
app = FastAPI(title="Todo")


app.include_router(auth.router) # Include the auth router for authentication endpoints


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

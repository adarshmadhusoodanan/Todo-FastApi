import uvicorn
from fastapi import FastAPI

<<<<<<< HEAD
from .database import create_db_and_tables

from .routes import auth
=======

from .database import create_db_and_tables, engine

>>>>>>> f6b54c0aebf55d60193e2b9fac10e519fb07bb77


# Create FastAPI app
app = FastAPI(title="Todo")


<<<<<<< HEAD
app.include_router(auth.router) # Include the auth router for authentication endpoints


=======
>>>>>>> f6b54c0aebf55d60193e2b9fac10e519fb07bb77
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

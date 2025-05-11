




from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.auth import get_current_user
from app.database import get_db
from app.models import Todo, TodoCreate, TodoRead, User


router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=TodoRead)
def create_todo(
    todo: TodoCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_todo = Todo(**todo.dict(), user_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@router.get("/", response_model=List[TodoRead])
def read_todos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.user_id == current_user.id).offset(skip).limit(limit)
    todos = db.exec(statement).all()
    return todos
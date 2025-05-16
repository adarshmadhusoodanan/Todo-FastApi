
from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.helper.auth import get_current_user
from app.db.database import get_db
from app.db.models import Todo, TodoRead, User


router = APIRouter(prefix="/todos", tags=["todos"])


#list all todos for the current user
@router.get("/", response_model=List[TodoRead])
def list_todos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.user_id == current_user.id).offset(skip).limit(limit)
    todos = db.exec(statement).all()
    return todos


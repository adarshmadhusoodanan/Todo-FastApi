





from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, col, select

from app.auth import get_current_user
from app.database import get_db
from app.models import Todo, TodoCreate, TodoRead, TodoUpdate, User


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

#list all todos for the current user
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


@router.get("/{todo_id}", response_model=TodoRead)
def read_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Verify ownership
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this todo")
        
    return todo


@router.get("/done/{done_status}", response_model=List[TodoRead])
def read_todos_by_status(
    done_status: bool,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = (
        select(Todo)
        .where(Todo.user_id == current_user.id, Todo.done == done_status)
        .offset(skip)
        .limit(limit)
    )
    todos = db.exec(statement).all()
    return todos


#mark a todo as completed
@router.patch("/{todo_id}/complete", response_model=TodoRead)
def mark_todo_as_completed(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_todo = db.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    # Verify ownership
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")
    
    db_todo.done = True
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

#edit a todo
@router.patch("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int, 
    todo_update: TodoUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_todo = db.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    # Verify ownership
    if db_todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this todo")
    
    todo_data = todo_update.dict(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


#delete a todo
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    todo = db.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
        
    # Verify ownership
    if todo.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this todo")
    
    db.delete(todo)
    db.commit()
    return None
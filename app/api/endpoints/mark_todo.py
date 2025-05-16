

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.helper.auth import get_current_user
from app.db.database import get_db
from app.db.models import Todo, TodoRead, User


router = APIRouter(prefix="/todos", tags=["todos"])


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

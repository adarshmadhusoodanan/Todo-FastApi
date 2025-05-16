



from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from app.helper.auth import get_current_user
from app.db.database import get_db
from app.db.models import Todo, User


router = APIRouter(prefix="/todos", tags=["todos"])

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
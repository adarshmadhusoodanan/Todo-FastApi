

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.database import get_db
from app.db.models import BlacklistedToken, User
from app.helper.auth import get_current_user , oauth2_scheme


router = APIRouter(tags=["authentication"]) 


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user),token: str = Depends(oauth2_scheme) ,db: Session = Depends(get_db)):
    # Ensure the current user is valid
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user"
        )
    
    # Check if token is already blacklisted
    statement = select(BlacklistedToken).where(BlacklistedToken.token == token)
    existing_token = db.exec(statement).first()
    
    if existing_token:
        return {"detail": "Already logged out"}
    
    # Add token to blacklist
    blacklisted_token = BlacklistedToken(token=token)
    db.add(blacklisted_token)
    db.commit()
    
    return {"detail": f"User {current_user.email} successfully logged out"}

# @router.post("/logout")
# def logout(
#     current_user: User = Depends(get_current_user), 
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Check if token is already blacklisted
#         statement = select(BlacklistedToken).where(BlacklistedToken.token == token)
#         existing_token = db.exec(statement).first()
        
#         if existing_token:
#             return {"detail": "Already logged out"}
        
#         # Add token to blacklist
#         blacklisted_token = BlacklistedToken(token=token)
#         db.add(blacklisted_token)
#         db.commit()
        
#         return {"detail": "Successfully logged out"}
#     except Exception as e:
#         db.rollback()  # Rollback the transaction in case of error
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Logout failed: {str(e)}"
#         )
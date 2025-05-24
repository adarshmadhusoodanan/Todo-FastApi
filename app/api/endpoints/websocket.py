# Add this to your main FastAPI application file (e.g., main.py)

from fastapi import APIRouter, WebSocket , Depends
from sqlmodel import Session


from app.db.database import get_db


from app.helper.broadcast import websocket_endpoint


router = APIRouter(tags=["websocket"])

# Add WebSocket route
@router.websocket("/ws")
async def websocket_route(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    await websocket_endpoint(websocket, token, db)

from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlmodel import Session
from typing import Dict, List
import json
import logging
from datetime import datetime

from app.db.database import get_db  
from app.helper.auth import get_current_user_from_token_ws
from app.db.models import User

# Set up logging
logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Store active connections with user info
        # Format: {user_id: {"websocket": websocket, "user": user_object}}
        self.active_connections: Dict[int, Dict] = {}
    
    async def connect(self, websocket: WebSocket, user: User):
        """Accept WebSocket connection and store user info"""
        await websocket.accept()
        self.active_connections[user.id] = {
            "websocket": websocket,
            "user": user
        }
        logger.info(f"User {user.name} (ID: {user.id}) connected")
        
        # Notify other users about new connection
        await self.broadcast_user_status(user, "joined", exclude_user_id=user.id)
    
    def disconnect(self, user_id: int):
        """Remove connection for a user"""
        if user_id in self.active_connections:
            user = self.active_connections[user_id]["user"]
            del self.active_connections[user_id]
            logger.info(f"User {user.name} (ID: {user_id}) disconnected")
            return user
        return None
    
    async def send_personal_message(self, message: str, user_id: int):
        """Send message to a specific user"""
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]["websocket"]
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Error sending message to user {user_id}: {e}")
                # Remove dead connection
                self.disconnect(user_id)
    
    async def broadcast_message(self, message: dict, exclude_user_id: int = None):
        """Broadcast message to all connected users except the sender"""
        message_str = json.dumps(message)
        dead_connections = []
        
        for user_id, connection_info in self.active_connections.items():
            # Skip the sender
            if exclude_user_id and user_id == exclude_user_id:
                continue
                
            websocket = connection_info["websocket"]
            try:
                await websocket.send_text(message_str)
            except Exception as e:
                logger.error(f"Error broadcasting to user {user_id}: {e}")
                dead_connections.append(user_id)
        
        # Clean up dead connections
        for user_id in dead_connections:
            self.disconnect(user_id)
    
    async def broadcast_user_status(self, user: User, status: str, exclude_user_id: int = None):
        """Broadcast user status changes (joined/left)"""
        status_message = {
            "type": "user_status",
            "user_id": user.id,
            "user_name": user.name,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_message(status_message, exclude_user_id)
    
    def get_active_users(self) -> List[dict]:
        """Get list of currently active users"""
        return [
            {
                "id": user_id,
                "name": connection_info["user"].name,
                "email": connection_info["user"].email
            }
            for user_id, connection_info in self.active_connections.items()
        ]
    
    def get_user_count(self) -> int:
        """Get count of active users"""
        return len(self.active_connections)

# Global connection manager instance
manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, token: str, db: Session = Depends(get_db)):
    """
    WebSocket endpoint for authenticated real-time messaging
    Usage: ws://localhost:8000/ws?token=your_jwt_token
    """
    try:
        # Authenticate user using token
        user = get_current_user_from_token_ws(token, db)
        
        # Connect user
        await manager.connect(websocket, user)
        
        # Send welcome message with active users list
        welcome_message = {
            "type": "welcome",
            "message": f"Welcome {user.name}! You are now connected.",
            "active_users": manager.get_active_users(),
            "user_count": manager.get_user_count(),
            "timestamp": datetime.utcnow().isoformat()
        }
        await websocket.send_text(json.dumps(welcome_message))
        
        # Listen for messages
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                # Validate message structure
                if "message" not in message_data:
                    error_msg = {"type": "error", "message": "Invalid message format"}
                    await websocket.send_text(json.dumps(error_msg))
                    continue
                
                # Create broadcast message
                broadcast_data = {
                    "type": "message",
                    "user_id": user.id,
                    "user_name": user.name,
                    "message": message_data["message"],
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                # Broadcast to all other users
                await manager.broadcast_message(broadcast_data, exclude_user_id=user.id)
                
                # Send confirmation back to sender
                confirmation = {
                    "type": "message_sent",
                    "message": "Message broadcasted successfully",
                    "timestamp": datetime.utcnow().isoformat()
                }
                await websocket.send_text(json.dumps(confirmation))
                
            except json.JSONDecodeError:
                error_msg = {"type": "error", "message": "Invalid JSON format"}
                await websocket.send_text(json.dumps(error_msg))
            except Exception as e:
                logger.error(f"Error processing message from user {user.id}: {e}")
                error_msg = {"type": "error", "message": "Error processing message"}
                await websocket.send_text(json.dumps(error_msg))
                
    except Exception as auth_error:
        # Authentication failed
        logger.warning(f"WebSocket authentication failed: {auth_error}")
        await websocket.close(code=4001, reason="Authentication failed")
        return
    
    except WebSocketDisconnect:
        # Handle normal disconnection
        pass
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        # Clean up connection
        if 'user' in locals():
            disconnected_user = manager.disconnect(user.id)
            if disconnected_user:
                # Notify other users about disconnection
                await manager.broadcast_user_status(disconnected_user, "left")



async def send_message_to_user(user_id: int, message: dict):
    """Send a message to a specific user (useful for notifications)"""
    message_str = json.dumps(message)
    await manager.send_personal_message(message_str, user_id)


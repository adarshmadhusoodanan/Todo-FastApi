from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import EmailStr



# Model schemas for User
class UserBase(SQLModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# Model schemas for Todo
class TodoBase(SQLModel):
    description: str
    deadline: datetime
    done: bool = False

class TodoCreate(TodoBase):
    pass



class TodoRead(TodoBase):
    id: int
    user_id: int



class TodoUpdate(SQLModel):
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    done: Optional[bool] = None


# Database models
class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    password: str
    
    todos: List["Todo"] = Relationship(back_populates="user")

class Todo(TodoBase, table=True):
    __tablename__ = "todos"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="users.id")
    
    user: Optional[User] = Relationship(back_populates="todos")



# Model for blacklisted tokens
class BlacklistedToken(SQLModel, table=True):
    __tablename__ = "blacklisted_tokens"
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    token: str = Field(unique=True, index=True)
    blacklisted_on: datetime = Field(default_factory=datetime.utcnow)

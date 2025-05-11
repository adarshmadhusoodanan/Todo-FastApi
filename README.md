# Todo FastAPI Application

A Todo application with user authentication built with FastAPI and PostgreSQL.

## Features

- User registration and authentication
- JWT token-based security
- Todo item management with deadlines

## Technologies Used

- FastAPI - Modern, fast web framework for building APIs with Python
- SQLModel - ORM for SQL databases designed for Python type annotations
- PostgreSQL - Relational database for data storage
- JWT - Authentication using JSON Web Tokens
- Pydantic - Data validation using Python type annotations

## Project Setup

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. Clone the repository:
   ```bash
   git clone 
   cd Todo-FastApi
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Create a PostgreSQL database named `Tododb`
   - Update the connection string in `app/database.py` if necessary

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Access the API documentation at `http://127.0.0.1:8000/docs`

## API Endpoints

### Authentication

- `POST /register` - Register a new user
- `POST /token` - Login and get access token
- `POST /logout` - Blacklist current token

### Todos

- `POST /todos/` - Create a new todo
- `GET /todos/` - List user's todos
- `GET /todos/{todo_id}` - Get a specific todo
- `GET /done/{done_status}` - group by completed todo
- `PATCH /{todo_id}/complete` - mark as completed
- `PATCH /todos/{todo_id}` - edit a todo
- `DELETE /todos/{todo_id}` - delete a todo


## Security

- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- Token blacklisting for logout functionality
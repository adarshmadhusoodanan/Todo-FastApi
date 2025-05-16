# Todo API with FastAPI & SQLModel

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)  
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)  

A complete Todo application with user authentication built using **FastAPI**, **SQLModel**, and **PostgreSQL**.

---

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Development](#development)
- [License](#license)

---

## Features

### User Management
- User registration with email and password.
- Secure password hashing using **bcrypt**.
- JWT token-based authentication.
- Token blacklisting for secure logout.

### Todo Management
- Create, list, update, and delete todo items.
- Filter todos by completion status.
- Mark todos as complete.
- Todo ownership verification.

### Security
- Environment variable configuration.
- JWT token expiration.
- Secure password storage.
- CSRF protection via JWT.

---

## Technologies

- **Python 3.9+**
- **FastAPI** - Modern, fast web framework.
- **SQLModel** - SQL databases with Python objects.
- **PostgreSQL** - Powerful relational database.
- **JWT** - JSON Web Tokens for authentication.
- **Bcrypt** - Password hashing.
- **Uvicorn** - ASGI server.
- **Pydantic** - Data validation.
- **Python-dotenv** - Environment variable management.

---

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.9 or later installed.
- PostgreSQL database server running.
- pip package manager.
- Basic understanding of REST APIs.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/todo-fastapi.git
   cd todo-fastapi
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

1. Copy the sample environment file:
   ```bash
   cp .env.sample .env
   ```

2. Edit the `.env` file with your configuration:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
   SECRET_KEY=your-secure-secret-key-here
   ALGORITHM=HS256
   ```

   - `DATABASE_URL`: Your PostgreSQL connection string.
   - `SECRET_KEY`: A secure secret for JWT token signing.
   - `ALGORITHM`: JWT algorithm (default: HS256).

---

## Database Setup

1. Create a PostgreSQL database:
   ```bash
   createdb todo_db
   ```

2. The application will automatically create tables on the first run.

---

## Running the Application

Start the development server:
```bash
python run.py
```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## API Endpoints

### Authentication
| Method | Endpoint   | Description              |
|--------|------------|--------------------------|
| POST   | `/register`| Register a new user      |
| POST   | `/token`   | Login and get access token |
| POST   | `/logout`  | Logout and blacklist token |

### Todos
| Method | Endpoint                  | Description                  |
|--------|---------------------------|------------------------------|
| GET    | `/todos/`                 | List all todos for current user |
| GET    | `/todos/done/{status}`    | Filter todos by completion status |
| POST   | `/todos/`                 | Create a new todo            |
| PATCH  | `/todos/{todo_id}`        | Update a todo                |
| PATCH  | `/todos/{todo_id}/complete` | Mark todo as completed       |
| DELETE | `/todos/{todo_id}`        | Delete a todo                |

---

## Authentication

The API uses **JWT (JSON Web Tokens)** for authentication:

1. Register a user at `/register`.
2. Login at `/token` to get an access token.
3. Use the token in requests:
   ```http
   Authorization: Bearer <your-token>
   ```
4. Logout at `/logout` to invalidate the token.

---

## Development

### Project Structure
```
.
├── app/
│   ├── api/
│   │   ├── endpoints/      # All API endpoint routers
│   │   ├── deps.py         # Dependencies
│   │   └── routes.py       # Main router
│   ├── db/
│   │   ├── database.py     # DB connection
│   │   └── models.py       # Data models
│   ├── helper/
│   │   └── auth.py         # Authentication utilities
│   └── main.py             # FastAPI app
├── requirements.txt        # Dependencies
└── run.py                  # Application entry point
```

---
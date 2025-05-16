from fastapi import APIRouter


from app.api.endpoints import completed_todos, create_todo, delete_todo, edit_todo, list_todos, login, logout, mark_todo, signup


router = APIRouter()

# Include all endpoint routers
router.include_router(signup.router)
router.include_router(login.router)
router.include_router(logout.router)

router.include_router(create_todo.router)
router.include_router(list_todos.router)
router.include_router(completed_todos.router)
router.include_router(mark_todo.router)

router.include_router(delete_todo.router)
router.include_router(edit_todo.router)
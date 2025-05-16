from fastapi import APIRouter


from app.api.endpoints import create_todo, login, logout, signup


router = APIRouter()

# Include all endpoint routers
router.include_router(signup.router)
router.include_router(login.router)
router.include_router(logout.router)

router.include_router(create_todo.router)
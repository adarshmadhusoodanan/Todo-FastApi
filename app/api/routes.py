from fastapi import APIRouter


from app.api.endpoints import login, signup


router = APIRouter(prefix="/api/todos")

# Include all endpoint routers
router.include_router(signup.router)
router.include_router(login.router)
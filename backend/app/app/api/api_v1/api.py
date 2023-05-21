from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    email,
    jobs,
    login,
    users,
    proxy,
    services,
)

api_router = APIRouter()
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(proxy.router, prefix="/proxy", tags=["proxy"])
api_router.include_router(services.router, prefix="/service", tags=["service"])
api_router.include_router(email.router, prefix="/email", tags=["email"])

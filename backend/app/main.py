from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router
from backend.app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "Software-only industrial bearing signal analysis and predictive "
        "maintenance research platform."
    ),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(router)


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    return {"name": "EdgeMaint-X", "docs": "/docs", "health": "/api/v1/health"}

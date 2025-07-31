from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer

from backend.app.api import auth, file_analysis
from backend.app.core.database import Base, engine

from backend.app.models import user, file

app = FastAPI()
app.include_router(auth.router)
app.include_router(file_analysis.router)

# Crea las tablas si no existen (sólo para desarrollo)
Base.metadata.create_all(bind=engine)

# Define el esquema OAuth2 para la documentación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="ThreatWatch API",
        version="1.0.0",
        description="API de autenticación para ThreatWatch",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {}
                }
            }
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"OAuth2PasswordBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi





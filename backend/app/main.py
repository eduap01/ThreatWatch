from fastapi import FastAPI


from backend.app.api import auth
from backend.app.core.databse import Base, engine

app = FastAPI()
app.include_router(auth.router)

# Crea las tablas si no existen (sólo para desarrollo)
Base.metadata.create_all(bind=engine)
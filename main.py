from fastapi import FastAPI
from app.db import init_db
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.init_db import Base
from app.models import user, admin
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=init_db.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


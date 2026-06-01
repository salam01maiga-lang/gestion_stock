from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, produits, ventes, historiques, categories, dashboard, alertes
from database import engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

app.include_router(users.router)
app.include_router(produits.router)
app.include_router(ventes.router)
app.include_router(alertes.router)
app.include_router(categories.router)
app.include_router(historiques.router)
app.include_router(dashboard.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_methods= ["*"],
    allow_headers= ["*"]
)
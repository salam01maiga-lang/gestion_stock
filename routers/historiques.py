from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.dependencies import get_db, get_current_user
import models
from datetime import date

router = APIRouter()

@router.get("/historique")
def historique_vente(date_filter: date = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = db.query(models.Vente)
    if date_filter:
        query = query.filter(models.Vente.date_vente >= date_filter)
    return query.all()
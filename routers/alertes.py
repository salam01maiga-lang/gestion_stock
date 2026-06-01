from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.dependencies import get_current_user, get_db
import schemas, models

router = APIRouter()

@router.get("/alertes")
def alertes_produits(db: Session = Depends(get_db), current: models.User = Depends(get_current_user)):
    return db.query(models.Produit).filter(models.Produit.stock <= models.Produit.seuil_alerte).all()
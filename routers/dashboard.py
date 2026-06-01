from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from utils.dependencies import get_current_user, get_db
from datetime import date
import models, schemas

router = APIRouter()

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    produits = db.query(models.Produit).count()
    ventes = db.query(models.Vente).filter(models.Vente.date_vente >= date.today()).count()
    produits_alerte = db.query(models.Produit).filter(models.Produit.stock <= models.Produit.seuil_alerte).count()
    chiffre_affaires = db.query(func.sum(models.Vente.prix_total)).scalar() or 0
    return {
        "produits": produits,
        "ventes": ventes,
        "produit en alerte": produits_alerte,
        "chiffre_affaires": chiffre_affaires
    }
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.dependencies import get_db, get_current_user
import schemas, models

router = APIRouter()

@router.get("/categories")
def afficher_categories(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Categorie).all()

@router.post("/categories", status_code= 201)
def creer_categorie(categorie: schemas.CategorieCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_categorie = models.Categorie(
        nom = categorie.nom,
        description = categorie.description
    )
    db.add(new_categorie)
    db.commit()
    db.refresh(new_categorie)
    return new_categorie

@router.delete("/categories/{id}")
def supprimer_categorie(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    categorie = db.query(models.Categorie).filter(models.Categorie.id == id).first()
    if not categorie:
        raise HTTPException(status_code= 404, detail= "Categorie introuvable")
    db.delete(categorie)
    db.commit()
    return {"message": f"Categorie {id} supprimer avec succes"}

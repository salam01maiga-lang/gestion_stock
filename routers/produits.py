from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.dependencies import get_db, get_current_user
import schemas, models

router = APIRouter()


@router.get("/produits")
def afficher_produits(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Produit).all()

@router.get("/produits/{id}")
def afficher_produit(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    produit = db.query(models.Produit).filter(models.Produit.id == id).first()
    if not produit:
        raise HTTPException(status_code= 404, detail= "Produit introuvable")
    return produit

@router.post("/produits", status_code= 201)
def create_produit(produit: schemas.ProduitCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_produit = models.Produit(
        nom = produit.nom,
        description = produit.description,
        prix_unitaire = produit.prix_unitaire,
        stock = produit.stock,
        seuil_alerte = produit.seuil_alerte,
        categorie_id = produit.categorie_id
    )
    db.add(new_produit)
    db.commit()
    db.refresh(new_produit)
    return new_produit

@router.put("/produits/{id}")
def modifier_produit(id: int, produit: schemas.ProduitCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    produit_edit = db.query(models.Produit).filter(models.Produit.id == id).first()
    if not produit_edit:
        raise HTTPException(status_code= 404, detail= "Produit introuvable")
    produit_edit.nom = produit.nom
    produit_edit.description = produit.description
    produit_edit.prix_unitaire = produit.prix_unitaire
    produit_edit.stock = produit.stock
    produit_edit.seuil_alerte = produit.seuil_alerte
    produit_edit.categorie_id = produit.categorie_id

    db.commit()
    db.refresh(produit_edit)
    return produit_edit

@router.delete("/produits/{id}")
def supprimer_produit(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    produit = db.query(models.Produit).filter(models.Produit.id == id).first()
    if not produit:
        raise HTTPException(status_code= 404, detail= "Produit introuvable")
    db.delete(produit)
    db.commit()
    return {"message": f"Produit {id} supprimer avec succes"}
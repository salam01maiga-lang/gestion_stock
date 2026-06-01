from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.dependencies import get_db, get_current_user
import models, schemas

router = APIRouter()

@router.get("/ventes")
def afficher_ventes(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Vente).all()

@router.post("/ventes", status_code= 201)
def faire_vente(vente: schemas.VenteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    new_vente = models.Vente(
        user_id = current_user.id,
        prix_total = 0
    )
    db.add(new_vente)
    db.flush()
    
    prix_total = 0

    for ligne in vente.lignevente:
        produit = db.query(models.Produit).filter(models.Produit.id == ligne.produit_id).first()
        if not produit:
            raise HTTPException(status_code= 404, detail= "Produit introuvable")
        if produit.stock < ligne.quantite:
            raise HTTPException(status_code= 400, detail= f"Stock insuffisant pour {produit.nom}")
    
        produit.stock -= ligne.quantite
        prix_total += produit.prix_unitaire * ligne.quantite

        new_ligne = models.LigneVente(
            vente_id = new_vente.id,
            produit_id= ligne.produit_id,
            quantite= ligne.quantite
        )
        db.add(new_ligne)

    new_vente.prix_total = prix_total
    db.commit()
    db.refresh(new_vente)
    return new_vente
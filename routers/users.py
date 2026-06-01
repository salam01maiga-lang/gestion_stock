from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from utils.dependencies import get_db, get_current_user
import models, schemas, utils.authFonction

router = APIRouter()

@router.post("/incription", response_model = schemas.UserResponse, status_code = 201)
def inscription(user: schemas.UserRegister, db: Session = Depends(get_db)):
    user_existant = db.query(models.User).filter(models.User.email == user.email).first()
    if user_existant:
        raise HTTPException(status_code= 400, detail= "email existant")
    mdp_hasher = utils.authFonction.hasher_mdp(user.mot_de_passe)
    new_user = models.User(
        username = user.username,
        email = user.email,
        mot_de_passe = mdp_hasher
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_existant = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user_existant:
        raise HTTPException(status_code= 401, detail= "Username incorrect")
    if not utils.authFonction.verifier_hash(form_data.password, user_existant.mot_de_passe):
        raise HTTPException(status_code= 401, detail= "Mot de passe incorrect")
    token = utils.authFonction.creer_token({"sub": user_existant.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model= schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user


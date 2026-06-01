from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal
import models, utils.authFonction

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email_token = utils.authFonction.verifier_token(token)
    if not email_token:
        raise HTTPException(status_code= 401, detail= "token invalide")
    user = db.query(models.User).filter(models.User.email == email_token).first()
    if not user:
        raise HTTPException(status_code= 404, detail= "Utilisateur introuvable")
    return user
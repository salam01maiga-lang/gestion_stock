from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from utils.config import settings

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated= "auto")

def hasher_mdp(mdp: str):
    return pwd_context.hash(mdp)

def verifier_hash(mdp: str, mdp_hasher):
    return pwd_context.verify(mdp, mdp_hasher)

def creer_token(data: dict):
    donnee = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes = settings.EXPIRATION)
    donnee.update({"exp": expiration})
    return jwt.encode(donnee, settings.SECRET_KEY, algorithm= settings.ALGORITHM)

def verifier_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms= [settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None
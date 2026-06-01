from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "hnb0#9fb&wobf)nwbdb!dwon`~0020dbeob_wdnob-|eo bo3$iwv&gwi^wi25.>wibud?oi2b"
ALGORITHM = "HS256"
EXPIRATION = 30

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated= "auto")

def hasher_mdp(mdp: str):
    return pwd_context.hash(mdp)

def verifier_hash(mdp: str, mdp_hasher):
    return pwd_context.verify(mdp, mdp_hasher)

def creer_token(data: dict):
    donnee = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes = EXPIRATION)
    donnee.update({"exp": expiration})
    return jwt.encode(donnee, SECRET_KEY, algorithm= ALGORITHM)

def verifier_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None
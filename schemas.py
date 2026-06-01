from pydantic import BaseModel
from datetime import datetime

#======= USER ========
class UserRegister(BaseModel):
    username: str
    email: str
    mot_de_passe: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    mot_de_passe: str

#======= Categorie ========
class CategorieCreate(BaseModel):
    nom: str
    description: str | None = None

class CategorieResponse(BaseModel):
    id: int
    nom: str
    description: str | None = None

    class Config:
        from_attributes = True

#======= Produit =========
class ProduitCreate(BaseModel):
    nom: str
    prix_unitaire: float
    description: str
    stock: int
    seuil_alerte: int
    categorie_id: int

class ProduitResponse(BaseModel):
    id: int
    nom: str
    prix_unitaire: float
    description: str
    stock: int
    seuil_alerte: int
    categorie: CategorieResponse

    class Config:
        from_attributes = True

#======== LIGNEVENTE =========
class LigneVenteCreate(BaseModel):
    quantite: int
    produit_id: int

class LigneVenteResponse(BaseModel):
    id: int
    quantite: int
    produit: ProduitResponse

    class Config:
        from_attributes = True

#======== VENTE ========
class VenteCreate(BaseModel):
    lignevente: list[LigneVenteCreate]

class VenteResponse(BaseModel):
    id: int
    date_vente: datetime
    prix_total: float
    user: UserResponse
    lignevente: list[LigneVenteResponse]


    class Config:
        from_attributes = True


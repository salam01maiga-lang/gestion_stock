from sqlalchemy import Integer, DateTime, Text, String, Float, ForeignKey, Column
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key= True, )
    username = Column(String(32), nullable= False, unique= True, index= True)
    email = Column(String(100), nullable = False, unique= True, index= True)
    mot_de_passe = Column(String(100), nullable= False)

    ventes = relationship("Vente", back_populates= "user")

class Categorie(Base):
    __tablename__ = "categorie"
    id = Column(Integer, primary_key= True)
    nom = Column(String(100), nullable= False, unique= True)
    description = Column(Text)

    produits = relationship("Produit", back_populates="categorie")

class Produit(Base):
    __tablename__ = "produit"
    id = Column(Integer, primary_key= True)
    nom = Column(String(100), nullable= False, index= True)
    description = Column(Text)
    prix_unitaire = Column(Float, nullable= False)
    stock = Column(Integer, default= 0)
    seuil_alerte = Column(Integer)
    categorie_id = Column(Integer, ForeignKey("categorie.id"))

    categorie = relationship("Categorie", back_populates="produits")
    ligneVente = relationship("LigneVente", back_populates= "produit")

class Vente(Base):
    __tablename__ = "vente"
    id = Column(Integer, primary_key= True)
    date_vente = Column(DateTime, default= datetime.utcnow)
    prix_total = Column(Float)
    user_id = Column(Integer, ForeignKey("user.id"), index= True)

    user = relationship("User", back_populates= "ventes")
    ligneVente = relationship("LigneVente", back_populates= "vente")

    
class LigneVente(Base):
    __tablename__ = "LigneVente"
    id = Column(Integer, primary_key= True)
    quantite = Column(Integer, nullable= False)
    vente_id = Column(Integer, ForeignKey("vente.id"), index= True)
    produit_id = Column(Integer, ForeignKey("produit.id"), index= True)

    produit = relationship("Produit", back_populates="ligneVente")
    vente = relationship("Vente", back_populates="ligneVente")
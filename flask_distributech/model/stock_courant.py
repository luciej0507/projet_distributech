from pydantic import BaseModel

class StockCourant(BaseModel):
    id: int = None # par défaut None pour l'auto-incrémentation
    nom_produit: str
    stock_initial: int
    nb_exemplaire: int
    stock_courant: int
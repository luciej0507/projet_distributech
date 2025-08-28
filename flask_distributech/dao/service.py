from dao.connexion import Connexion
from model.stock_courant import StockCourant

# La classe Service hérite de Connexion
class Service (Connexion): 

    @classmethod
    def showStock(cls, stock_courant: StockCourant): # stock_courant : instance de StockCourant 
        try:
            cls.connect()
            #values = [StockCourant.nom_produit, StockCourant.stock_initial, StockCourant.nb_exemplaire, StockCourant.stock_courant]
            query = "SELECT * FROM stock_courant"   # Requête SQL pour récupérer le stock courant de tous les produits
            cls.cursor.execute(query) #, values)    # on exécute la requête SQL
            result = cls.cursor.fetchall()          # on récupère tous les résultats
            return result

        except Exception as err:
            print(f"Le stock courant n'a pu être rétrouvé, {err}")
        finally: # quoiqu'il arrive, on ferme la connexion
            cls.close()
from dotenv import load_dotenv
import os
import pandas as pd
import mysql.connector

load_dotenv()

DB_HOST      = os.getenv("DB_HOST")
DB_ROOT      = os.getenv("DB_ROOT")
DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
DB_NAME      = os.getenv("DB_NAME")
DB_USER      = os.getenv("DB_USER")
DB_PASSWORD  = os.getenv("DB_PASSWORD")

# connexion à la base SQL
admin_cnx = mysql.connector.connect(
    host=DB_HOST,
    user=DB_ROOT,      
    password=DB_ROOT_PASSWORD,
    database=DB_NAME
)
admin_cursor = admin_cnx.cursor()


# Fichier CSV de l'état des stocks par produit
query_csv = """
SELECT p.id, p.nom_produit, p.quantite AS stock_initial, IFNULL(c.nb_exemplaire, 0) AS nb_exemplaire, (quantite - IFNULL(c.nb_exemplaire, 0)) AS stock_courant 
FROM produits p
LEFT JOIN commandes_produits cp ON p.id = cp.produit
LEFT JOIN commandes c ON cp.commande = c.id
"""

df_csv_stocks = pd.read_sql(query_csv, admin_cnx)

df_csv_stocks.to_csv("etat_stocks.csv", index=False, encoding="utf-8")
print("Fichier 'etat_stocks.csv' généré avec succès.")


# Commit et fermeture
admin_cnx.commit()
admin_cursor.close()
admin_cnx.close()
import pandas as pd
import sqlite3
import random
import mysql.connector
#from datetime import datetime

# à mettre en loadenv()
DB_HOST      = 'localhost'
DB_ROOT      = 'root'
DB_ROOT_PASSWORD = 'example'
DB_NAME      = 'distributech'
DB_USER      = 'exemple'
DB_PASSWORD  = 'exemple'

# Récupération du chemin du fichier csv
csv_path = "./data/commande_revendeur_tech_express.csv"
# Extraction des données du fichier CSV
df_csv = pd.read_csv(csv_path)
# print(df_csv)


# Connexion à la base source SQLite pour l'extraction des données
sqlite_path = "/home/luciej/iadev/distributech/data/base_stock.sqlite"
conn = sqlite3.connect(sqlite_path)
cur = conn.cursor()

# connexion à la base SQL
admin_cnx = mysql.connector.connect(
    host=DB_HOST,
    user=DB_ROOT,      
    password=DB_ROOT_PASSWORD,
    database=DB_NAME
)
admin_cursor = admin_cnx.cursor()


# Extraction des données de la base SQLite
query_produits = "SELECT t.product_id, t.product_name, t.cout_unitaire, n.quantity, n.date_production FROM produit t JOIN production n ON t.product_id = n.product_id"
query_revendeurs_regions = "SELECT r.region_id, r.revendeur_name, n.region_name FROM region n JOIN revendeur r ON n.region_id = r.region_id"

### pour table intermédiaire : on récupère les id de la table commandes dans la db distributech
query_commandes = "SELECT id FROM commandes"
df_query_commandes = pd.read_sql(query_commandes, admin_cnx) # envoyer les id dans un dataframe

query_stocks = "SELECT id FROM stocks"
df_query_stocks = pd.read_sql(query_stocks, admin_cnx)


commandes_product = df_csv[['product_id']] # déclarer l'id du product dans la variable
#print(commandes_product)
commande_id = df_query_commandes[['id']] # déclarer l'id dans la variable pour pouvoir l'envoyer en base de données
#print(commande_id)

# on insère la colonne index en position 0 dans les 2 df
commandes_product.insert(0, "index", [0, 1, 2, 3, 4], False)
commande_id.insert(0, "index", [0, 1, 2, 3, 4], False)
#print(commande_id)

# on remplace l'index automatique du df par la colonne index + inplace=True : fait la modification direct sur le df
commandes_product.set_index('index', inplace=True)
commande_id.set_index('index', inplace=True)

# on fait la fusion en utilisant les index des 2 df
new_df = df_query_commandes.merge(commandes_product, how='right', left_index=True, right_index=True) # left_index=True, right_index=True = on fait la fusion en utilisant les index des 2 df
new_df.drop_duplicates()
#print(new_df)

""" # on insère les données dans la table intermédiaire commandes_produits
for row in new_df.itertuples(index = False):
    produit = row.product_id
    commande = row.id
    admin_cursor.execute(
        "INSERT INTO commandes_produits (produit, commande) VALUES (%s, %s)", (produit, commande)
    )
 """


# mettre les données extraites dans des dataframes pour les manipuler avec pandas pour les mettre dans la base sql
df_produits = pd.read_sql(query_produits, conn)
#print(df_produits)
df_revendeurs_regions = pd.read_sql(query_revendeurs_regions, conn)
#print(df_revendeurs_regions)

# accéder à une ou plusieurs colonnes des dataframes
# (attention : si un seul [] = tuple= pas bon, il faut en mettre 2 [[]] pour que ce soit une liste)
#regions = df_revendeurs_regions[['region_name']]

######## REGIONS
# on supprime les doublons dans la colonne 'region_name'
""" regions_unique = df_revendeurs_regions['region_name'].drop_duplicates()

# on insère les données dans la table "regions"
for nom_region in regions_unique:
    admin_cursor.execute(
        "INSERT INTO regions (nom_region) VALUES (%s)", (nom_region,) # important de passer en tuple (donc , apres nom_region)
    )


######## REVENDEURS
revendeurs = df_revendeurs_regions[['revendeur_name','region_id']]
# on insère les données dans la table "revendeurs"
for row in revendeurs.itertuples(index=False):  # on parcours les deux colonnes du df en même temps + on ignore les id du dataframe
    nom_revendeur = row.revendeur_name  # on extrait noms des revendeurs dans la table revendeur_name de la base sqlite
    region = row.region_id  # contient l’identifiant numérique de la région (clé étrangère vers la table regions)
    admin_cursor.execute(
        "INSERT INTO revendeurs (nom_revendeur, region) VALUES (%s, %s)", (nom_revendeur, region,)
    ) """

""" 
######## COMMANDES
commandes = df_csv[['numero_commande','commande_date','quantity','revendeur_id']]
# on insère les données dans la table "commandes"
for row in commandes.itertuples(index=False):
    num_commande = row.numero_commande
    date_commande = row.commande_date
    nb_exemplaire = row.quantity
    revendeur = row.revendeur_id
    admin_cursor.execute(
        "INSERT INTO commandes (num_commande, date_commande, nb_exemplaire, revendeur) VALUES (%s, %s, %s,%s)",
        (num_commande, date_commande, nb_exemplaire, revendeur)
    ) """

""" ###### PRODUITS
produits = df_produits[['product_name', 'cout_unitaire','quantity']]
 
for row in produits.itertuples(index=False):
    nom_produit = row.product_name
    cout_unitaire = row.cout_unitaire
    quantite = row.quantity
    admin_cursor.execute(
        "INSERT INTO produits (nom_produit, cout_unitaire, quantite) VALUES (%s, %s, %s)",
        (nom_produit, cout_unitaire, quantite)
    ) """

# avec ajout de "product_id" à la place de "id"
""" produits = df_produits[['product_id','product_name', 'cout_unitaire','quantity']]
 
for row in produits.itertuples(index=False):
    id = row.product_id
    nom_produit = row.product_name
    cout_unitaire = row.cout_unitaire
    quantite = row.quantity
    admin_cursor.execute(
        "INSERT INTO produits (id, nom_produit, cout_unitaire, quantite) VALUES (%s, %s, %s, %s)",
        (id, nom_produit, cout_unitaire, quantite)
    ) """

######## Stocks
""" stock_date = df_produits[['date_production']].copy()    # on crée un nouveau DataFrame indépendant
stock_date.insert(0, "index", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], False) # on insère une colonne index
stock_date.set_index('index', inplace=True)
stock = pd.to_datetime(stock_date['date_production'], yearfirst=True) # on convertit une string en objet datetime (avec l'année en 1er)
#print(stock)

# on insère les date_production dans la table stocks 
for date_prod in stock:
    admin_cursor.execute(
        "INSERT INTO stocks (stock_date) VALUES (%s)", (date_prod,) # important de passer en tuple (donc , apres nom_region)
    )
 """


####### Tables intermédiares :
# stock_produits

# on récupére donnée product_id qu'on met dans variable produit_id
produit_id = df_produits[['product_id']]
produit_id.insert(0, "index", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], False) # création colonne index
produit_id.set_index('index', inplace=True)

# on récupère les id de la table stocks
stocks_id = df_query_stocks[['id']]
stocks_id.insert(0, "index", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], False) # création colonne index
stocks_id.set_index('index', inplace=True)

# on merge les 2 df
table_intermediaire = produit_id.merge(stocks_id, how='right', left_index=True, right_index=True)
#print(table_intermediaire)

# insertion dans la table stock_produits
for row in table_intermediaire.itertuples(index=False):
    produit = row.product_id
    stock = row.id
    admin_cursor.execute(
        "INSERT INTO stock_produits (produit, stock) VALUES (%s, %s)",
        (produit, stock)
    )


# Commit et fermeture
#admin_cnx.commit()
#admin_cursor.close()
#admin_cnx.close()






# faire en sorte que la base sql soit maj chaque semaine ?

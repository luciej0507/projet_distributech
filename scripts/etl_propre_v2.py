from dotenv import load_dotenv
import os
import pandas as pd
import sqlite3
import random
import mysql.connector

def main():
    load_dotenv()

    admin_cnx = None
    admin_cursor = None
    conn =  None

    try:
        # Connexion à la base SQL
        DB_HOST      = os.getenv("DB_HOST")
        DB_ROOT      = os.getenv("DB_ROOT")
        DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
        DB_NAME      = os.getenv("DB_NAME")
        DB_USER      = os.getenv("DB_USER")
        DB_PASSWORD  = os.getenv("DB_PASSWORD")


        admin_cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_ROOT,      
            password=DB_ROOT_PASSWORD,
            database=DB_NAME
        )
        admin_cursor = admin_cnx.cursor()

        # Connexion à la base source SQLite
        sqlite_path = "/home/luciej/iadev/distributech/data/base_stock.sqlite"
        conn = sqlite3.connect(sqlite_path)

        # Récupération du chemin du fichier csv pour l'extraction des données
        csv_path = "./data/commande_revendeur_tech_express.csv"



        ######## EXTRACTION

        # Extraction des données du fichier CSV
        df_csv = pd.read_csv(csv_path)
        # print(df_csv)

        # Extraction des données de la base SQLite
        query_produits = "SELECT t.product_id, t.product_name, t.cout_unitaire, n.quantity, n.date_production FROM produit t JOIN production n ON t.product_id = n.product_id"
        query_revendeurs_regions = "SELECT r.region_id, r.revendeur_name, n.region_name FROM region n JOIN revendeur r ON n.region_id = r.region_id"

        # mettre les données extraites dans des dataframes pour les manipuler avec pandas pour les mettre dans la base sql
        df_produits = pd.read_sql(query_produits, conn)
        #print(df_produits)
        df_revendeurs_regions = pd.read_sql(query_revendeurs_regions, conn)
        #print(df_revendeurs_regions)

        #### définir les réfèrences des produits et des revendeurs :
        reference = []
        for i in range(0, 20):
            # Set the required length
            length_of_string = 8
            sample_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            # k is an argument which will set the length
            generated_string = ''.join(random.choices(sample_str, k = length_of_string))  
            reference.append(generated_string)
        # print(reference)

        # on sépare la liste reference en 2 listes avec 10 refs
        ref_produit = reference[:10]
        ref_revendeur = reference[10:]
        #print(ref_produit)
        #print(ref_revendeur)

        # on met les listes dans des df
        df_reference = pd.DataFrame(reference, columns=['reference'])
        df_ref_produit = pd.DataFrame(ref_produit, columns=['ref_produit'])
        df_ref_revendeur = pd.DataFrame(ref_revendeur, columns=['ref_revendeur'])
        #print(df_reference)
        #print(df_ref_produit)
        #print(df_ref_revendeur)



        ############ TRANSFORMATION et LOADING

        #### Table REGIONS
        # accéder à une ou plusieurs colonnes des dataframes
        regions = df_revendeurs_regions[['region_name']]

        # on supprime les doublons dans la colonne 'region_name'
        regions_unique = regions['region_name'].drop_duplicates()

        # on insère les données dans la table "regions"
        for nom_region in regions_unique:
            admin_cursor.execute(
                "INSERT INTO regions (nom_region) VALUES (%s)", (nom_region,) # important de passer en tuple (donc , apres nom_region)
            )

        #### Table REVENDEURS
        revendeurs = df_revendeurs_regions[['revendeur_name','region_id']]
        ref_revendeurs = df_ref_revendeur[['ref_revendeur']]

        # on merge les 2 df
        revendeurs = df_revendeurs_regions.merge(
            df_ref_revendeur[['ref_revendeur']], 
            left_index=True, 
            right_index=True
        )

        # on insère les données dans la table "revendeurs"
        for row in revendeurs.itertuples(index=False):  # on parcours les deux colonnes du df en même temps + on ignore les id du dataframe
            nom_revendeur = row.revendeur_name  # on extrait noms des revendeurs dans la table revendeur_name de la base sqlite
            ref_revendeur = row.ref_revendeur
            region = row.region_id  # contient l’identifiant numérique de la région (clé étrangère vers la table regions)
            admin_cursor.execute(
                "INSERT INTO revendeurs (nom_revendeur, ref_revendeur, region) VALUES (%s, %s, %s)", (nom_revendeur, ref_revendeur, region,)
            )

        #### Table COMMANDES
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
            )

        #### Table PRODUITS
        produits = df_produits[['product_id','product_name', 'cout_unitaire','quantity']]
        ref_produits = df_ref_produit[['ref_produit']]

        # on merge les 2 df
        produits = df_produits.merge(
            df_ref_produit[['ref_produit']], 
            left_index=True, 
            right_index=True
        )

        for row in produits.itertuples(index=False):
            id = row.product_id
            ref_produit = row.ref_produit
            nom_produit = row.product_name
            cout_unitaire = row.cout_unitaire
            quantite = row.quantity
            admin_cursor.execute(
                "INSERT INTO produits (id, ref_produit, nom_produit, cout_unitaire, quantite) VALUES (%s, %s, %s, %s, %s)",
                (id, ref_produit, nom_produit, cout_unitaire, quantite)
            )

        #### Table Stocks
        stock_date = df_produits[['date_production']].copy()    # on crée un nouveau DataFrame indépendant
        stock_date.insert(0, "index", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], False) # on insère une colonne index
        stock_date.set_index('index', inplace=True)
        stock = pd.to_datetime(stock_date['date_production'], yearfirst=True) # on convertit une string en objet datetime (avec l'année en 1er)
        #print(stock)

        # on insère les date_production dans la table stocks 
        for date_prod in stock:
            admin_cursor.execute(
                "INSERT INTO stocks (stock_date) VALUES (%s)", (date_prod,) # important de passer en tuple (donc , apres nom_region)
            )

        ###### Tables Intermédiaires :
        #### Table stock_produits

        # on récupère les id de la table stocks dans la db distributech
        query_stocks = "SELECT id FROM stocks"
        df_query_stocks = pd.read_sql(query_stocks, admin_cnx)

        # on récupére donnée product_id qu'on met dans la variable produit_id
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


        #### Table commandes_produits
        query_commandes = "SELECT id FROM commandes"
        df_query_commandes = pd.read_sql(query_commandes, admin_cnx) # envoyer les id dans un dataframe

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

        # on insère les données dans la table intermédiaire commandes_produits
        for row in new_df.itertuples(index = False):
            produit = row.product_id
            commande = row.id
            admin_cursor.execute(
                "INSERT INTO commandes_produits (produit, commande) VALUES (%s, %s)", (produit, commande)
            )

        # Commit et fermeture
        admin_cnx.commit()
        print("ETL terminé avec succès")

    except mysql.connector.Error as e:
        print(f"Erreur MySQL : {e}")
    except sqlite3.Error as e:
        print(f"Erreur SQLite : {e}")
    except FileNotFoundError as e:
        print(f"Fichier introuvable : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")
    finally:
        if admin_cursor:
            admin_cursor.close()
        if admin_cnx:
            admin_cnx.close()
        if conn:
            conn.close()
        print("Toutes les connexions sont fermées.")

if __name__ == "__main__":
    main()

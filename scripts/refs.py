import random
import pandas as pd
import mysql.connector

DB_HOST      = 'localhost'
DB_ROOT      = 'root'
DB_ROOT_PASSWORD = 'example'
DB_NAME      = 'distributech'
DB_USER      = 'exemple'
DB_PASSWORD  = 'exemple'

# connexion à la base SQL
admin_cnx = mysql.connector.connect(
    host=DB_HOST,
    user=DB_ROOT,      
    password=DB_ROOT_PASSWORD,
    database=DB_NAME
)
admin_cursor = admin_cnx.cursor()


# définir les réfèrences des produits et des revendeurs

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
""" df_reference = pd.DataFrame(reference, columns=['reference'])
print(df_reference) """

df_ref_produit = pd.DataFrame(ref_produit, columns=['ref_produit'])
df_ref_revendeur = pd.DataFrame(ref_revendeur, columns=['ref_revendeur'])
#print(df_ref_produit)
#print(df_ref_revendeur)


# insérer les references dans les tables produits et revendeurs
# table produits:

ref_produits = df_ref_produit[['ref_produit']]

for row in ref_produits.itertuples(index=False):
    ref_produit = row.ref_produit
    admin_cursor.execute(
        "INSERT INTO produits (ref_produit) VALUES (%s)", (ref_produit,)
    )

# Commit et fermeture
admin_cnx.commit()
#admin_cursor.close()
#admin_cnx.close()
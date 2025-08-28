import mysql.connector as mysqlpyth

bdd = None
cursor = None

# Fonction pour se connecter à la base de données
def connexion():
    global bdd
    global cursor

    bdd = mysqlpyth.connect(user='root', password='example', host='localhost', 
                            port="3306", database='distributech')
    cursor = bdd.cursor()

# Fonction pour fermer la connexion
def deconnexion():
    global bdd
    global cursor

    cursor.close()
    bdd.close()

# Fonction pour lire le stock courant depuis la vue "stock_courant"
def lire_stock():
    global cursor
    
    connexion()
    query = "SELECT * FROM stock_courant"
    cursor.execute(query)
    stocks = []
    for enregistrement in cursor :
        stock = {}
        stock['id'] = enregistrement[0]
        stock['nom_produit'] = enregistrement[1]
        stock['stock_initial'] = enregistrement[2]
        stock['nb_exemplaire'] = enregistrement[3]
        stock['stock_courant'] = enregistrement[4]
        stocks.append(stock)
        
    deconnexion()
    return stocks

from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

load_dotenv()

DB_HOST      = os.getenv("DB_HOST")
DB_ROOT      = os.getenv("DB_ROOT")
DB_ROOT_PASSWORD = os.getenv("DB_ROOT_PASSWORD")
DB_NAME      = os.getenv("DB_NAME")
DB_USER      = os.getenv("DB_USER")
DB_PASSWORD  = os.getenv("DB_PASSWORD")


def main():
    try:
        # Connexion en admin pour créer la base et l'utilisateur
        admin_cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_ROOT,
            password=DB_ROOT_PASSWORD
        )
        admin_cursor = admin_cnx.cursor()

        # Création de la base
        admin_cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            + "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        print(f"Base `{DB_NAME}` créée ou déjà existante.")

        # Création de l'utilisateur et attribution des droits
        admin_cursor.execute(
            f"CREATE USER IF NOT EXISTS '{DB_USER}'@'%' "
            f"IDENTIFIED BY '{DB_PASSWORD}'"
        )
        admin_cursor.execute(
            f"GRANT ALL PRIVILEGES ON `{DB_NAME}`.* "
            f"TO '{DB_USER}'@'%'"
        )
        admin_cursor.execute("FLUSH PRIVILEGES")
        admin_cnx.commit()
        admin_cursor.close()
        admin_cnx.close()
        print(f"Utilisateur `{DB_USER}`@`%` créé/mis à jour.")

    except Error as err:
        print(f"[Erreur admin] {err}")
        return
    
    try:
        # Connexion en tant que nouvel utilisateur sur la DB créée
        user_cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        user_cursor = user_cnx.cursor()

        # Création des tables
        statements = [
            # Table regions
            """
            CREATE TABLE IF NOT EXISTS regions (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nom_region VARCHAR(50) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table revendeurs
            """
            CREATE TABLE IF NOT EXISTS revendeurs (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nom_revendeur VARCHAR(50) NOT NULL,
                ref_revendeur VARCHAR(50) NOT NULL,
                region INT NOT NULL,
                FOREIGN KEY (region) REFERENCES regions(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table produits
            """
            CREATE TABLE IF NOT EXISTS produits (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                ref_produit VARCHAR(50) NOT NULL,
                nom_produit VARCHAR(50) NOT NULL,
                cout_unitaire DECIMAL(10,1) NOT NULL,
                quantite INT NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table stocks
            """
            CREATE TABLE IF NOT EXISTS stocks (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                stock_date DATE NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table commandes
            """
            CREATE TABLE IF NOT EXISTS commandes (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                num_commande VARCHAR(20) NOT NULL,
                date_commande DATE NOT NULL,
                nb_exemplaire INT NOT NULL,
                revendeur INT NOT NULL,
                FOREIGN KEY (revendeur) REFERENCES revendeurs(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table de liaison stock_produits
            """
            CREATE TABLE IF NOT EXISTS stock_produits (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                produit INT NOT NULL,
                stock INT NOT NULL,
                KEY idx_produit (produit),
                KEY idx_stock (stock),
                FOREIGN KEY (stock) REFERENCES stocks(id),
                FOREIGN KEY (produit) REFERENCES produits(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table de liaison commandes_produits
            """
            CREATE TABLE IF NOT EXISTS commandes_produits (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                produit INT NOT NULL,
                commande INT NOT NULL,
                KEY idx_produit (produit),
                KEY idx_commande (commande),
                FOREIGN KEY (commande) REFERENCES commandes(id),
                FOREIGN KEY (produit) REFERENCES produits(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        ]

        for stmt in statements:
            user_cursor.execute(stmt)
            print("→ OK :", stmt.strip().split()[2])

        user_cnx.commit()
        user_cursor.close()
        user_cnx.close()
        print("Initialisation de la base terminée avec succès.")

    except Error as err:
        print(f"[Erreur user] {err}")

if __name__ == "__main__":
    main()
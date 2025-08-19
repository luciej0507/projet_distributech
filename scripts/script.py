#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error

DB_HOST      = 'localhost'
DB_ROOT      = 'root'
DB_ROOT_PASSWORD = 'example'
DB_NAME      = 'exemple'
DB_USER      = 'exemple'
DB_PASSWORD  = 'exemple'


def main():
    try:
        # 1. Connexion en admin pour créer la base et l'utilisateur
        admin_cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_ROOT,      
            password=DB_ROOT_PASSWORD
        )
        admin_cursor = admin_cnx.cursor() # je me connecte en tant que admin et je récupère le cursor
        
        # Création de la base
        admin_cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        print(f"Base `{DB_NAME}` créée ou déjà existante.")
        
        # Création de l'utilisateur et attribution des droits
        admin_cursor.execute(
            f"CREATE USER IF NOT EXISTS '{DB_USER}'@'%' " # création utilisateur au lieu de root + respecter format sql avec '{DB_USER}'@'%'
            f"IDENTIFIED BY '{DB_PASSWORD}'"
        )
        admin_cursor.execute(
            f"GRANT ALL PRIVILEGES ON `{DB_NAME}`.* " # '*' signifie qu'on donne les droits sur toute la base
            f"TO '{DB_USER}'@'%'"
        )
        admin_cursor.execute("FLUSH PRIVILEGES")
        admin_cnx.commit() # à faire quand on a fait plsrs requêtes
        admin_cursor.close()
        admin_cnx.close() # on ferme cursor et la BD
        print(f"Utilisateur `{DB_USER}`@`%` créé/mis à jour.")

    except Error as err:
        print(f"[Erreur admin] {err}") #message erreur de la bd
        return # si message d'erreur, on arrête là, la suite n'est pas éxécutée

    try:
        # 2. Connexion en tant que nouvel utilisateur sur la DB créée
        user_cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER, # plus root, mais utilisateur
            password=DB_PASSWORD,
            database=DB_NAME
        )
        user_cursor = user_cnx.cursor()

        # 3. Création des tables et insertion des données
        statements = [
            # Table sites
            """
            CREATE TABLE IF NOT EXISTS sites (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                ville VARCHAR(50) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table utilisateurs
            """
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                prenom VARCHAR(50) NOT NULL,
                nom VARCHAR(50) NOT NULL,
                naissance INT(4) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Table de liaison
            """
            CREATE TABLE IF NOT EXISTS utilisateurs_sites (
                utilisateur INT NOT NULL,
                site INT NOT NULL,
                KEY idx_site (site),
                KEY idx_utilisateur (utilisateur),
                FOREIGN KEY (site) REFERENCES sites(id),
                FOREIGN KEY (utilisateur) REFERENCES utilisateurs(id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            # Insertion de quelques données
            "INSERT INTO sites (id, ville) VALUES "
            "(1, 'Port-Réal'), (2, 'Essos'), (4, 'Le Mur');",
            "INSERT INTO utilisateurs (id, prenom, nom, naissance) VALUES "
            "(1, 'Tyrion', 'Lannister', 2000),"
            "(2, 'Daenerys', 'Targaryen', 2002),"
            "(3, 'Jon', 'Snow', 2002),"
            "(4, 'Jaime', 'Lannister', 1998);",
            "INSERT INTO utilisateurs_sites (utilisateur, site) VALUES "
            "(1, 1), (2, 1), (2, 2), (3, 4);"
        ]

        for stmt in statements:
            user_cursor.execute(stmt) # python vérifie toutes les requêtes en ram et ensuite il commit
            print("→ OK :", stmt.strip().split()[2])  # affiche un mot-clé indicatif
        
        user_cnx.commit()
        user_cursor.close()
        user_cnx.close()
        print("Initialisation de la base terminée avec succès.")

    except Error as err:
        print(f"[Erreur user] {err}")


if __name__ == "__main__":
    main()

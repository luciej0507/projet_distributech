import mysql.connector as mysql
from dao.config import BDD_USER, BDD_PASSWORD, BDD_HOST, BDD_DATABASE

class Connexion:
    @classmethod # avec ça, pas besoin de def init
    def connect(cls):
            cls.connection = mysql.connect(
                host=BDD_HOST,
                user=BDD_USER,
                password=BDD_PASSWORD,
                database=BDD_DATABASE
            )
            cls.cursor = cls.connection.cursor(dictionary=True) #?


    @classmethod
    def close(cls):
        if cls.connection is not None:
            cls.connection.close()
            cls.cursor.close()
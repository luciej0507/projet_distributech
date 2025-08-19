import mysql.connector
import pandas as pd

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

query = "SELECT * FROM stock_courant"

df_query = pd.read_sql(query, admin_cnx)
print(df_query)



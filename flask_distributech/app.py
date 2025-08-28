from flask import Flask, render_template
from dao.service import Service

# Création de l'application Flask
app = Flask(__name__)

# Route principale : affiche la page d'accueil (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route "/stock_courant" : 
# appelle le service SQL avec la méthode Service.showStock pour récupérer les données
# envoie ces données au template stock_courant.html
@app.route("/stock_courant")
def stock_courant():
    stocks = Service.showStock(stock_courant)
    return render_template("stock_courant.html", stocks=stocks)

if __name__ == "__main__":
    app.run(debug=True)
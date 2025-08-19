-- Le stock courant peut être reconstitué à date, 
-- par une soustraction des commandes du stock général.

-- creation de la vue stock_courant :
SELECT p.id, p.nom_produit, p.quantite, c.nb_exemplaire, (quantite - nb_exemplaire) AS stock_courant 
FROM produits p
JOIN commandes_produits cp ON p.id = cp.produit
JOIN commandes c ON cp.commande = c.id 
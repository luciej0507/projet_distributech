-- Le stock courant peut être reconstitué à date, 
-- par une soustraction des commandes du stock général.

-- creation de la vue stock_courant :
SELECT p.id, p.nom_produit, p.quantite as stock_initial, IFNULL (c.nb_exemplaire, 0) as nb_exemplaire, (quantite - IFNULL (c.nb_exemplaire, 0)) AS stock_courant 
FROM produits p
LEFT JOIN commandes_produits cp ON p.id = cp.produit
LEFT JOIN commandes c ON cp.commande = c.id 
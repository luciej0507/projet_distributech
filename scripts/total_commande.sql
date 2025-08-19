-- création de la vue total_commande

SELECT c.num_commande, p.id, p.cout_unitaire, c.nb_exemplaire, (cout_unitaire * nb_exemplaire) AS total_commande
FROM produits p
JOIN commandes_produits cp ON p.id = cp.produit
JOIN commandes c ON cp.commande = c.id 
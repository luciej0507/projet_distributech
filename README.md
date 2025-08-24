# Projet Distributech  

## Description  
Distributech est un projet visant à centraliser et automatiser la gestion des stocks et des commandes d’un réseau de revendeurs en équipements électroniques.  
Il repose sur une **base de données relationnelle SQL** et un **pipeline ETL hebdomadaire** intégrant des données issues de fichiers CSV et d’une base SQLite locale.  

Objectif : fournir une vision claire et à jour de l’état des stocks et de l’historique des commandes.  

---

## Fonctionnalités  
- Création d’une **base de données SQL centralisée**.
- Mise en place du **processus ETL**:
- Extraction des données depuis :  
  - Fichiers CSV  
  - Base SQLite locale 
- Nettoyage et transformation des données (dates, doublons, cohérence).  
- Chargement dans la base SQL centralisée.  
- Génération d’un **rapport CSV hebdomadaire** de l’état des stocks par produit.  

---

## Prérequis  
- **Matériel** : PC classique (Windows, Linux, macOS) avec ≥ 5 Go libres et connexion internet stable.  
- **Logiciel** :  
  - Python ≥ 3.12  
  - Bibliothèques Python : `pandas`, `sqlite3`, `mysql-connector`  
  - Bases de données :  
    - Locale : SQLite  
    - Centralisée : MySQL  

---

## Langage & Technologies  
- **Langage principal** : Python  
- **Bases de données** : SQLite (local) & MySQL (centralisée)  
- **ETL** : pandas + scripts Python  

---

## Licence
Ce projet est sous licence MIT

---

## Mots-clés
`ETL` · `Python` · `SQL` · `SQLite` · `MySQL` · `CSV` · `Data Pipeline` · `Automatisation`

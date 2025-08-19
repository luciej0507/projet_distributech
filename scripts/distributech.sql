#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: Region
#------------------------------------------------------------

CREATE TABLE Region(
        id         Int  Auto_increment  NOT NULL ,
        Nom_region Varchar (50) NOT NULL
	,CONSTRAINT Region_PK PRIMARY KEY (id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Revendeur
#------------------------------------------------------------

CREATE TABLE Revendeur(
        id            Int  Auto_increment  NOT NULL ,
        Nom_vendeur   Varchar (50) NOT NULL ,
        Ref_revendeur Varchar (50) NOT NULL ,
        id_Region     Int NOT NULL
	,CONSTRAINT Revendeur_PK PRIMARY KEY (id)

	,CONSTRAINT Revendeur_Region_FK FOREIGN KEY (id_Region) REFERENCES Region(id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Produits
#------------------------------------------------------------

CREATE TABLE Produits(
        id            Int  Auto_increment  NOT NULL ,
        Ref_produit   Varchar (50) NOT NULL ,
        Nom_produit   Varchar (50) NOT NULL ,
        Cout_unitaire Decimal NOT NULL ,
        Quantite      Int NOT NULL
	,CONSTRAINT Produits_PK PRIMARY KEY (id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Stock
#------------------------------------------------------------

CREATE TABLE Stock(
        id         Int  Auto_increment  NOT NULL ,
        Stock_date Datetime NOT NULL
	,CONSTRAINT Stock_PK PRIMARY KEY (id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: Commandes
#------------------------------------------------------------

CREATE TABLE Commandes(
        id             Int  Auto_increment  NOT NULL ,
        Num_commande   Varchar (20) NOT NULL ,
        Date_commande  Datetime NOT NULL ,
        Nb_exemplaire  Int NOT NULL ,
        Total_commande Decimal NOT NULL ,
        id_Revendeur   Int NOT NULL
	,CONSTRAINT Commandes_PK PRIMARY KEY (id)

	,CONSTRAINT Commandes_Revendeur_FK FOREIGN KEY (id_Revendeur) REFERENCES Revendeur(id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: fait_partie
#------------------------------------------------------------

CREATE TABLE fait_partie(
        id          Int NOT NULL ,
        id_Produits Int NOT NULL
	,CONSTRAINT fait_partie_PK PRIMARY KEY (id,id_Produits)

	,CONSTRAINT fait_partie_Stock_FK FOREIGN KEY (id) REFERENCES Stock(id)
	,CONSTRAINT fait_partie_Produits0_FK FOREIGN KEY (id_Produits) REFERENCES Produits(id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: appartient
#------------------------------------------------------------

CREATE TABLE appartient(
        id          Int NOT NULL ,
        id_Produits Int NOT NULL
	,CONSTRAINT appartient_PK PRIMARY KEY (id,id_Produits)

	,CONSTRAINT appartient_Commandes_FK FOREIGN KEY (id) REFERENCES Commandes(id)
	,CONSTRAINT appartient_Produits0_FK FOREIGN KEY (id_Produits) REFERENCES Produits(id)
)ENGINE=InnoDB;


-- Project: Healthcare Data Warehouse BI
-- Description: Creation des tables du schéma en étoile
-- SGBD: MySQL

CREATE DATABASE IF NOT EXISTS hopital_dw;
USE hopital_dw;

CREATE TABLE Patient (
   id_patient INT,
   nom VARCHAR(50) NOT NULL,
   prenom VARCHAR(50),
   sexe VARCHAR(10),
   date_naissance DATE NOT NULL,
   ville VARCHAR(50),
   PRIMARY KEY (id_patient)
);

CREATE TABLE Service (
   id_service INT,
   nom_service VARCHAR(50),
   type_service VARCHAR(50),
   capacite_lits INT,
   PRIMARY KEY (id_service)
);

CREATE TABLE Medecin (
   id_medecin INT,
   nom_medecin VARCHAR(50),
   prenom_medecin VARCHAR(50),
   specialite VARCHAR(50),
   ancienete INT NOT NULL,
   PRIMARY KEY (id_medecin)
);

CREATE TABLE Temps (
   id_temps INT,
   date_complete DATE,
   jour INT,
   mois INT,
   trimestre INT,
   annee INT,
   PRIMARY KEY (id_temps)
);

CREATE TABLE Sejour (
   id_sejour INT,
   duree_sejour INT,
   cout_total DECIMAL(15,2),
   nombre_examens INT,
   id_temps INT NOT NULL,
   id_service INT NOT NULL,
   id_medecin INT NOT NULL,
   id_patient INT NOT NULL,
   PRIMARY KEY (id_sejour),
   CONSTRAINT fk_sejour_temps   FOREIGN KEY (id_temps)   REFERENCES Temps(id_temps),
   CONSTRAINT fk_sejour_service FOREIGN KEY (id_service) REFERENCES Service(id_service),
   CONSTRAINT fk_sejour_medecin FOREIGN KEY (id_medecin) REFERENCES Medecin(id_medecin),
   CONSTRAINT fk_sejour_patient FOREIGN KEY (id_patient) REFERENCES Patient(id_patient)
);

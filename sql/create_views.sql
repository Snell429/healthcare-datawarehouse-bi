-- Project: Healthcare Data Warehouse BI
-- Description: KPI views for hospital activity analysis
-- SGBD: MySQL

-- 1) Nombre de séjours par service
CREATE VIEW v_nb_sejours_par_service AS
SELECT 
  s.id_service,
  s.nom_service,
  COUNT(se.id_sejour) AS nb_sejours
FROM sejour se
JOIN service s ON se.id_service = s.id_service
GROUP BY s.id_service, s.nom_service;

-- 2) Durée moyenne de séjour par service
CREATE VIEW v_duree_moyenne_par_service AS
SELECT 
  s.id_service,
  s.nom_service,
  ROUND(AVG(se.duree_sejour), 2) AS duree_moyenne
FROM sejour se
JOIN service s ON se.id_service = s.id_service
GROUP BY s.id_service, s.nom_service;

-- 3) Coût total et coût moyen par service
CREATE VIEW v_cout_par_service AS
SELECT 
  s.id_service,
  s.nom_service,
  ROUND(SUM(se.cout_total), 2) AS cout_total_service,
  ROUND(AVG(se.cout_total), 2) AS cout_moyen_service
FROM sejour se
JOIN service s ON se.id_service = s.id_service
GROUP BY s.id_service, s.nom_service;

-- 4) Nombre de séjours par mois
CREATE VIEW v_nb_sejours_par_mois AS
SELECT 
  t.annee,
  t.mois,
  COUNT(se.id_sejour) AS nb_sejours
FROM sejour se
JOIN temps t ON se.id_temps = t.id_temps
GROUP BY t.annee, t.mois
ORDER BY t.annee, t.mois;

-- 5) Activité par médecin
CREATE VIEW v_activite_par_medecin AS
SELECT 
  m.id_medecin,
  m.nom_medecin,
  m.prenom_medecin,
  COUNT(se.id_sejour) AS nb_sejours
FROM sejour se
JOIN medecin m ON se.id_medecin = m.id_medecin
GROUP BY m.id_medecin, m.nom_medecin, m.prenom_medecin;

USE hopital_dw;

CREATE TABLE IF NOT EXISTS ml_predictions (
   id_prediction INT AUTO_INCREMENT,
   id_sejour INT NOT NULL,
   prediction_duree_sejour DECIMAL(10,2) NOT NULL,
   prediction_timestamp DATETIME NOT NULL,
   PRIMARY KEY (id_prediction),
   INDEX idx_ml_predictions_sejour (id_sejour),
   INDEX idx_ml_predictions_timestamp (prediction_timestamp)
);

CREATE OR REPLACE VIEW v_ml_predictions_latest AS
SELECT
    latest.id_prediction,
    latest.id_sejour,
    latest.prediction_duree_sejour,
    latest.prediction_timestamp,
    ml.nom_service,
    ml.type_service,
    ml.capacite_lits,
    ml.specialite,
    ml.ancienete,
    ml.sexe,
    ml.age,
    ml.ville,
    ml.mois,
    ml.trimestre,
    ml.annee,
    ml.nombre_examens,
    ml.cout_total,
    ml.duree_sejour
FROM ml_predictions latest
JOIN (
    SELECT
        id_sejour,
        MAX(prediction_timestamp) AS max_prediction_timestamp
    FROM ml_predictions
    GROUP BY id_sejour
) current_run
    ON latest.id_sejour = current_run.id_sejour
   AND latest.prediction_timestamp = current_run.max_prediction_timestamp
JOIN v_ml_dataset ml
    ON latest.id_sejour = ml.id_sejour;

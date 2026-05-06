from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from sqlalchemy import URL, create_engine

try:
    from config import load_env_file
except ImportError:
    from ml.config import load_env_file


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DATASET_PATH = BASE_DIR / "dataset.csv"
OUTPUT_PREDICTION_INPUT_PATH = BASE_DIR / "sample_prediction_input.csv"
SQL_QUERY = """
SELECT
    id_sejour,
    TRIM(REPLACE(REPLACE(nom_service, CHAR(13), ''), CHAR(10), '')) AS service,
    TRIM(REPLACE(REPLACE(type_service, CHAR(13), ''), CHAR(10), '')) AS type_service,
    capacite_lits,
    TRIM(REPLACE(REPLACE(specialite, CHAR(13), ''), CHAR(10), '')) AS specialite_medecin,
    ancienete AS ancienete_medecin,
    TRIM(REPLACE(REPLACE(sexe, CHAR(13), ''), CHAR(10), '')) AS sexe,
    age,
    TRIM(REPLACE(REPLACE(ville, CHAR(13), ''), CHAR(10), '')) AS ville,
    mois,
    trimestre,
    nombre_examens,
    cout_total,
    duree_sejour
FROM v_ml_dataset
"""


def get_mysql_url() -> URL:
    load_env_file()

    host = os.getenv("MYSQL_HOST", "localhost")
    port = os.getenv("MYSQL_PORT", "3306")
    database = os.getenv("MYSQL_DATABASE", "hopital_dw")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")

    if not user or not password:
        raise ValueError(
            "Variables d'environnement manquantes: MYSQL_USER et MYSQL_PASSWORD."
        )

    return URL.create(
        "mysql+mysqlconnector",
        username=user,
        password=password,
        host=host,
        port=int(port),
        database=database,
    )


def build_dataset() -> pd.DataFrame:
    engine = create_engine(get_mysql_url())
    with engine.connect() as connection:
        dataset = pd.read_sql(SQL_QUERY, connection)

    return dataset.sort_values(
        by=["trimestre", "mois", "service", "specialite_medecin"],
        ignore_index=True,
    )


def main() -> None:
    dataset = build_dataset()
    dataset.to_csv(OUTPUT_DATASET_PATH, index=False)
    dataset.drop(columns=["duree_sejour"]).head(10).to_csv(
        OUTPUT_PREDICTION_INPUT_PATH,
        index=False,
    )

    print("Dataset ML genere depuis MySQL.")
    print("Source SQL : v_ml_dataset")
    print(f"Dataset : {OUTPUT_DATASET_PATH}")
    print(f"Entree prediction : {OUTPUT_PREDICTION_INPUT_PATH}")
    print(f"Lignes dataset : {len(dataset)}")


if __name__ == "__main__":
    main()

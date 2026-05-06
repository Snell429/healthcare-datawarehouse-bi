from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
from sqlalchemy import text

try:
    from data_preparation import FEATURE_COLUMNS
    from mysql_utils import get_mysql_engine
except ImportError:
    from ml.data_preparation import FEATURE_COLUMNS
    from ml.mysql_utils import get_mysql_engine


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "artifacts" / "length_of_stay_model.joblib"
DEFAULT_INPUT_PATH = BASE_DIR / "sample_prediction_input.csv"
DEFAULT_OUTPUT_PATH = BASE_DIR / "predictions.csv"
DEFAULT_TARGET_TABLE = "ml_predictions"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Predire la duree de sejour pour de nouveaux patients."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Chemin du fichier CSV contenant les nouvelles observations.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Chemin du fichier CSV de sortie avec les predictions.",
    )
    parser.add_argument(
        "--write-mysql",
        action="store_true",
        help="Ecrit aussi les predictions dans MySQL.",
    )
    parser.add_argument(
        "--table",
        default=DEFAULT_TARGET_TABLE,
        help="Nom de la table MySQL cible pour les predictions.",
    )
    return parser.parse_args()


def write_predictions_to_mysql(predictions_df: pd.DataFrame, table_name: str) -> None:
    if "id_sejour" not in predictions_df.columns:
        raise ValueError(
            "La colonne id_sejour est requise pour ecrire les predictions dans MySQL."
        )

    mysql_ready = predictions_df[["id_sejour", "prediction_duree_sejour"]].copy()
    mysql_ready["prediction_timestamp"] = datetime.now(timezone.utc).replace(tzinfo=None)

    engine = get_mysql_engine()
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id_prediction INT AUTO_INCREMENT PRIMARY KEY,
        id_sejour INT NOT NULL,
        prediction_duree_sejour DECIMAL(10, 2) NOT NULL,
        prediction_timestamp DATETIME NOT NULL,
        INDEX idx_ml_predictions_sejour (id_sejour),
        INDEX idx_ml_predictions_timestamp (prediction_timestamp)
    )
    """

    with engine.begin() as connection:
        connection.execute(text(create_table_sql))
        mysql_ready.to_sql(table_name, con=connection, if_exists="append", index=False)


def main() -> None:
    args = parse_args()

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Le modele n'existe pas encore. Lancez d'abord model_training.py."
        )

    if not args.input.exists():
        raise FileNotFoundError(f"Fichier d'entree introuvable: {args.input}")

    model = joblib.load(MODEL_PATH)
    input_dataframe = pd.read_csv(args.input)
    predictions = model.predict(input_dataframe[FEATURE_COLUMNS])

    result = input_dataframe.copy()
    result["prediction_duree_sejour"] = predictions.round(2)
    result.to_csv(args.output, index=False)

    if args.write_mysql:
        write_predictions_to_mysql(result, args.table)

    print("Predictions generees.")
    print(f"Fichier source : {args.input}")
    print(f"Fichier resultat: {args.output}")
    if args.write_mysql:
        print(f"Table MySQL cible : {args.table}")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATASET_PATH = BASE_DIR / "dataset.csv"
TARGET_COLUMN = "duree_sejour"
IDENTIFIER_COLUMNS = ["id_sejour"]
FEATURE_COLUMNS = [
    "service",
    "type_service",
    "capacite_lits",
    "specialite_medecin",
    "ancienete_medecin",
    "sexe",
    "age",
    "ville",
    "mois",
    "trimestre",
    "nombre_examens",
    "cout_total",
]

REQUIRED_COLUMNS = [
    *IDENTIFIER_COLUMNS,
    *FEATURE_COLUMNS,
    TARGET_COLUMN,
]

NUMERIC_FEATURES = [
    "capacite_lits",
    "ancienete_medecin",
    "age",
    "mois",
    "trimestre",
    "nombre_examens",
    "cout_total",
]

CATEGORICAL_FEATURES = [
    "service",
    "type_service",
    "specialite_medecin",
    "sexe",
    "ville",
]


def load_dataset(dataset_path: Path | str = DEFAULT_DATASET_PATH) -> pd.DataFrame:
    dataset_path = Path(dataset_path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset introuvable: {dataset_path}")

    dataframe = pd.read_csv(dataset_path)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in dataframe.columns]
    if missing_columns:
        raise ValueError(
            "Le dataset est incomplet. Colonnes manquantes: "
            + ", ".join(missing_columns)
        )

    return dataframe


def split_features_target(dataframe: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    features = dataframe[FEATURE_COLUMNS].copy()
    target = dataframe[TARGET_COLUMN]
    return features, target


def build_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )

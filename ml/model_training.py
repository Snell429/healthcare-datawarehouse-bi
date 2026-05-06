from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.base import clone
from sklearn.ensemble import ExtraTreesRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

try:
    from build_dataset import main as build_dataset_main
    from data_preparation import build_preprocessor, load_dataset, split_features_target
except ImportError:
    from ml.build_dataset import main as build_dataset_main
    from ml.data_preparation import build_preprocessor, load_dataset, split_features_target


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "artifacts"
MODEL_PATH = MODEL_DIR / "length_of_stay_model.joblib"
METRICS_PATH = MODEL_DIR / "training_metrics.json"


def evaluate_candidate(name: str, estimator, X_train, y_train) -> dict:
    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor()),
            ("model", estimator),
        ]
    )
    scorer = "neg_mean_absolute_error"
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring=scorer)
    return {
        "name": name,
        "pipeline": pipeline,
        "cv_mae_mean": round(float(-cv_scores.mean()), 3),
        "cv_mae_std": round(float(cv_scores.std()), 3),
    }


def build_candidates():
    return [
        ("ridge", Ridge(alpha=1.0)),
        (
            "gradient_boosting",
            GradientBoostingRegressor(
                n_estimators=250,
                learning_rate=0.05,
                max_depth=3,
                random_state=42,
            ),
        ),
        (
            "random_forest",
            RandomForestRegressor(
                n_estimators=400,
                max_depth=12,
                min_samples_leaf=2,
                random_state=42,
            ),
        ),
        (
            "extra_trees",
            ExtraTreesRegressor(
                n_estimators=400,
                max_depth=12,
                min_samples_leaf=2,
                random_state=42,
            ),
        ),
    ]


def main() -> None:
    build_dataset_main()
    dataframe = load_dataset()
    features, target = split_features_target(dataframe)

    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
    )

    candidate_results = [
        evaluate_candidate(name, estimator, X_train, y_train)
        for name, estimator in build_candidates()
    ]
    best_candidate = min(candidate_results, key=lambda item: item["cv_mae_mean"])
    pipeline = clone(best_candidate["pipeline"])

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    metrics = {
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "selected_model": best_candidate["name"],
        "mae": round(mean_absolute_error(y_test, predictions), 3),
        "rmse": round(mse ** 0.5, 3),
        "r2": round(r2_score(y_test, predictions), 3),
        "candidate_models": [
            {
                "name": result["name"],
                "cv_mae_mean": result["cv_mae_mean"],
                "cv_mae_std": result["cv_mae_std"],
            }
            for result in candidate_results
        ],
    }

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print("Entrainement termine.")
    print(f"Modele selectionne : {best_candidate['name']}")
    print(f"Modele sauvegarde: {MODEL_PATH}")
    print(f"Metriques sauvegardees: {METRICS_PATH}")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

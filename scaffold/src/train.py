"""
Model training with MLflow experiment tracking.
================================================

CONTRACT — implement ``train_and_log`` so it trains several models, records each as an
MLflow run, selects a champion, and serialises it. Keep the signature.

Run as a module:  ``python -m src.train``
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import joblib
import mlflow
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from .data_prep import TARGET, add_features, load_and_clean

#: Where the champion model is written.
CHAMPION_PATH: str = "models/champion.pkl"


def train_and_log(df: pd.DataFrame, champion_path: str = CHAMPION_PATH) -> str:
    """Train 2-3 regressors, log them to MLflow, and save the champion.

    Must:
      - split features/target with NO leakage (``TARGET`` and leakage cols excluded from X),
      - train at least TWO models (e.g. LinearRegression, RandomForestRegressor,
        GradientBoostingRegressor),
      - for EACH model open an ``mlflow.start_run`` and log params + metrics
        (RMSE, MAE, R2) + the model artifact,
      - select the champion by the best held-out RMSE,
      - serialise the champion (e.g. ``joblib.dump``) to ``champion_path``.

    Args:
        df: Feature-engineered DataFrame (post :func:`add_features`).
        champion_path: Destination path for the serialised champion.

    Returns:
        The path the champion was written to.
    """
    y = df[TARGET]
    X = df.drop(columns=[TARGET, "dteday"])

    sort_idx = np.argsort(df["dteday"].values.astype(np.int64))
    X = X.iloc[sort_idx].reset_index(drop=True)
    y = y.iloc[sort_idx].reset_index(drop=True)

    split_point = int(0.8 * len(X))
    X_train, X_test = X.iloc[:split_point], X.iloc[split_point:]
    y_train, y_test = y.iloc[:split_point], y.iloc[split_point:]

    models = [
        ("LinearRegression", LinearRegression(), {}),
        (
            "RandomForest",
            RandomForestRegressor(n_estimators=100, random_state=42),
            {"n_estimators": 100, "random_state": 42},
        ),
        (
            "GradientBoosting",
            GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42),
            {"n_estimators": 100, "learning_rate": 0.1, "random_state": 42},
        ),
    ]

    Path(champion_path).parent.mkdir(parents=True, exist_ok=True)

    champion = None
    best_rmse = float("inf")

    for name, model, params in models:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae = float(mean_absolute_error(y_test, y_pred))
        r2 = float(r2_score(y_test, y_pred))

        with mlflow.start_run(run_name=name):
            mlflow.log_params(params)
            mlflow.log_metrics({"RMSE": rmse, "MAE": mae, "R2": r2})
            mlflow.sklearn.log_model(model, artifact_path="model")

        if rmse < best_rmse:
            best_rmse = rmse
            champion = model

    joblib.dump(champion, champion_path)
    return str(Path(champion_path).resolve())


def main(data_path: Optional[str] = None) -> str:
    """Entry point: clean -> feature-engineer -> train_and_log."""
    path = data_path or "data/hour.csv"
    df = add_features(load_and_clean(path))
    return train_and_log(df)


if __name__ == "__main__":
    print(f"Champion saved to: {main()}")
